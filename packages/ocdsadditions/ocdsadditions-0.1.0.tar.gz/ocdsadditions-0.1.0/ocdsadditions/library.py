import datetime
import glob
import json
import os
import tempfile
from collections import OrderedDict

import dateutil.parser
import ocdskit.combine  # type: ignore
import ocdskit.upgrade  # type: ignore
import ocdskit.util  # type: ignore
import requests
from flattentool import flatten, unflatten  # type: ignore
from jinja2 import Environment, PackageLoader, select_autoescape
from ocdsextensionregistry import ProfileBuilder  # type: ignore
from ocdskit.util import get_ocds_patch_tag  # type: ignore

from ocdsadditions.constants import LATEST_OCDS_SCHEMA_VERSION


def init_repository(directory: str):

    if not os.path.isdir(directory):
        os.makedirs(directory)

    ocids_directory = os.path.join(directory, "contracting_processes")
    if not os.path.isdir(ocids_directory):
        os.makedirs(ocids_directory)

    data: dict = {
        "config": {
            "package": {
                "publisher": {
                    "name": "",
                    "scheme": "",
                    "uid": "",
                    "uri": "",
                },
                "publicationPolicy": "",
                "license": "",
            }
        }
    }

    with open(os.path.join(directory, "ocdsadditions.json"), "w") as fp:
        json.dump(data, fp, indent=4)


class Repository:
    def __init__(self, directory_name: str):
        self._directory_name = directory_name
        if not os.path.isdir(directory_name):
            raise Exception("Directory does not exist")
        if not os.path.isfile(os.path.join(directory_name, "ocdsadditions.json")):
            raise Exception("Additions file not found")
        # TODO verify contents of ocdsadditions.json are correct schema?
        # If done here, no repo with broken config will work which is probably good

    def add_ocid(self, ocid):

        # TODO: Can we assume OCIDS are always valid directory names?
        ocid_directory = os.path.join(
            self._directory_name, "contracting_processes", ocid
        )
        if not os.path.isdir(ocid_directory):
            os.makedirs(ocid_directory)

        data: dict = {"ocid": ocid}

        with open(
            os.path.join(ocid_directory, "ocdsadditions_contracting_process.json"), "w"
        ) as fp:
            json.dump(data, fp, indent=4)

    def get_contracting_process(self, ocid: str):
        return ContractingProcess(self, ocid)

    def add_external_release_package(self, url: str):
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Non 200 response")

        package_data = r.json()
        if not ocdskit.util.is_release_package(package_data):
            raise Exception("Not a release package")

        releases = package_data["releases"]
        del package_data["releases"]
        for release in releases:
            if not ocdskit.util.is_release(release):
                raise Exception("Not a release")
            contracting_process = self.get_contracting_process(release["ocid"])
            contracting_process.add_release(package_data, release, url)

    def list_ocids(self) -> list:
        out: list = []
        for path in glob.glob(
            os.path.join(
                self._directory_name,
                "contracting_processes",
                "*",
                "ocdsadditions_contracting_process.json",
            )
        ):
            with open(path) as fp:
                data = json.load(fp)
                out.append(data["ocid"])
        return out

    def import_spreadsheet(self, import_filename: str):
        # Make sure filename & type is valid
        import_format: str = ""
        if import_filename.endswith(".xlsx"):
            import_format = "xlsx"
        elif import_filename.endswith(".ods"):
            import_format = "ods"
        else:
            raise Exception("Unknown import type")

        # Make release package
        output_temp_file = tempfile.mkstemp(suffix=".json", prefix="ocds-additions")
        os.close(output_temp_file[0])

        # Get JSON
        unflatten(
            import_filename,
            input_format=import_format,
            output_name=output_temp_file[1],
            root_id="ocid",
            root_list_path="releases",
        )
        with open(output_temp_file[1]) as fp:
            data = json.load(fp)

        # Process releases
        if not ocdskit.util.is_release_package(data):
            raise Exception("Can only import release packages")
        for release_data in data["releases"]:
            cp = self.get_contracting_process(release_data.get("ocid"))
            release = cp.get_release(release_data["id"])
            release.set_release_data(release_data)

        # Remove temp file
        os.unlink(output_temp_file[1])

    def get_config_package_data(self):
        with (open(os.path.join(self._directory_name, "ocdsadditions.json"))) as fp:
            data = json.load(fp)
        return data.get("config", {}).get("package", {})

    def get_config_party_data(self):
        with (open(os.path.join(self._directory_name, "ocdsadditions.json"))) as fp:
            data = json.load(fp)
        return data.get("config", {}).get("party", {})

    def get_config_add_party_to_our_releases_with_party_id(self):
        with (open(os.path.join(self._directory_name, "ocdsadditions.json"))) as fp:
            data = json.load(fp)
        return data.get("config", {}).get(
            "add_party_to_our_releases_with_party_id", None
        )

    def build_site(self, output_directory: str, url: str = ""):
        url_without_trailing_slash = url[:-1] if url.endswith("/") else url
        os.makedirs(output_directory, exist_ok=True)
        ocids: list = self.list_ocids()

        jinja_env = Environment(
            loader=PackageLoader("ocdsadditions"), autoescape=select_autoescape()
        )

        # Root files
        data = {
            "ocids": [
                {
                    "ocid": ocid,
                    "human_url": url_without_trailing_slash
                    + "/contracting_process/"
                    + ocid
                    + "/",
                    "api_url": url_without_trailing_slash
                    + "/contracting_process/"
                    + ocid
                    + "/api.json",
                }
                for ocid in ocids
            ],
            "package": self.get_config_package_data(),
            "party": self.get_config_party_data(),
        }
        with open(os.path.join(output_directory, "api.json"), "w") as fp:
            json.dump(data, fp, indent=4)
        with open(os.path.join(output_directory, "index.html"), "w") as fp:
            fp.write(
                jinja_env.get_template("index.html").render(
                    repository=self,
                    ocids=ocids,
                    url_without_trailing_slash=url_without_trailing_slash,
                    config_package=self.get_config_package_data(),
                    config_party=self.get_config_party_data(),
                )
            )

        # Contracting Processes
        for ocid in ocids:
            contracting_process = self.get_contracting_process(ocid)
            releases = contracting_process.list_releases()
            ocid_directory = os.path.join(output_directory, "contracting_process", ocid)
            os.makedirs(ocid_directory, exist_ok=True)
            data = {
                "ocid": ocid,
                "record_url": url_without_trailing_slash
                + "/contracting_process/"
                + ocid
                + "/record.json",
                "releases": [
                    {
                        "id": r.get_id(),
                        "release_package_url": url_without_trailing_slash
                        + "/contracting_process/"
                        + ocid
                        + "/release/"
                        + r._directory_name
                        + "/release_package.json",
                    }
                    for r in releases
                ],
            }
            with open(os.path.join(ocid_directory, "api.json"), "w") as fp:
                json.dump(data, fp, indent=4)

            with open(os.path.join(ocid_directory, "index.html"), "w") as fp:
                fp.write(
                    jinja_env.get_template("contracting_process/index.html").render(
                        repository=self,
                        ocid=ocid,
                        releases=releases,
                        url_without_trailing_slash=url_without_trailing_slash,
                    )
                )

            # Individual Releases
            for release in releases:
                release_directory = os.path.join(
                    ocid_directory, "release", release._directory_name
                )
                os.makedirs(release_directory, exist_ok=True)
                data = {}
                with open(os.path.join(release_directory, "api.json"), "w") as fp:
                    json.dump(data, fp, indent=4)
                release.write_release_package(
                    os.path.join(release_directory, "release_package.json")
                )

            # A record
            contracting_process.write_record_package(
                os.path.join(ocid_directory, "record.json")
            )


class ContractingProcess:
    def __init__(self, repository: Repository, ocid: str):
        self._repository = repository
        self._ocid = ocid

        self._ocid_directory = os.path.join(
            repository._directory_name, "contracting_processes", ocid
        )
        if not os.path.isdir(self._ocid_directory):
            raise Exception("OCID does not exist")
        if not os.path.isfile(
            os.path.join(self._ocid_directory, "ocdsadditions_contracting_process.json")
        ):
            raise Exception("OCID file not found")

    def add_release(self, package_data: dict, release: dict, source_url: str):
        datetime_object = dateutil.parser.parse(release["date"])
        # TODO: Can we assume IDS are always valid directory names?
        dir_name = datetime_object.strftime("%Y-%m-%d-%H-%M-%S") + "-" + release["id"]
        directory = os.path.join(self._ocid_directory, "releases", dir_name)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        data: dict = {
            "url": source_url,
            "id": release["id"],
            "date": datetime_object.isoformat(),
        }

        with open(os.path.join(directory, "ocdsadditions_release.json"), "w") as fp:
            json.dump(data, fp, indent=4)

        with open(os.path.join(directory, "package.json"), "w") as fp:
            json.dump(package_data, fp, indent=4)

        with open(os.path.join(directory, "release.json"), "w") as fp:
            json.dump(release, fp, indent=4)

    def add_empty_release(self, release_id: str):
        if self.does_release_id_exist(release_id):
            raise Exception("Release ID Already exists")
        datetime_object = datetime.datetime.now(datetime.timezone.utc)
        # TODO: Can we assume IDS are always valid directory names?
        dir_name = datetime_object.strftime("%Y-%m-%d-%H-%M-%S") + "-" + release_id
        directory = os.path.join(self._ocid_directory, "releases", dir_name)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        data: dict = {
            "id": release_id,
            "date": datetime_object.isoformat(),
        }

        # TODO add extensions info from existing releases
        # TODO add uri
        more_package_data = self._repository.get_config_package_data()
        package_data: dict = {
            "version": LATEST_OCDS_SCHEMA_VERSION,
            "publishedDate": datetime_object.isoformat(),
            "publisher": more_package_data.get("publisher", {}),
            "publicationPolicy": more_package_data.get("publicationPolicy", ""),
            "license": more_package_data.get("license", ""),
            "extensions": self.get_extensions_used(),
        }

        release_data: dict = {
            "ocid": self._ocid,
            "id": release_id,
            "date": datetime_object.isoformat(),
        }
        config_party_data = self._repository.get_config_party_data()
        config_add_party_to_our_releases_with_party_id = (
            self._repository.get_config_add_party_to_our_releases_with_party_id()
        )
        if config_add_party_to_our_releases_with_party_id and config_party_data:
            config_party_data["id"] = config_add_party_to_our_releases_with_party_id
            release_data["parties"] = [config_party_data]

        with open(os.path.join(directory, "ocdsadditions_release.json"), "w") as fp:
            json.dump(data, fp, indent=4)

        with open(os.path.join(directory, "package.json"), "w") as fp:
            json.dump(package_data, fp, indent=4)

        with open(os.path.join(directory, "release.json"), "w") as fp:
            json.dump(release_data, fp, indent=4)

        return Release(self, dir_name)

    def list_releases(self) -> list:
        out: list = []
        paths = glob.glob(
            os.path.join(
                self._ocid_directory, "releases", "*", "ocdsadditions_release.json"
            )
        )
        path_bits = [p.split("/")[-2] for p in paths]
        path_bits.sort()
        for path in path_bits:
            out.append(Release(self, path))
        return out

    def does_release_id_exist(self, release_id) -> bool:
        for path in glob.glob(
            os.path.join(
                self._ocid_directory, "releases", "*", "ocdsadditions_release.json"
            )
        ):
            with (open(path)) as fp:
                data = json.load(fp)
                if data["id"] == release_id:
                    return True
        return False

    def get_release(self, release_id: str):
        for path in glob.glob(
            os.path.join(
                self._ocid_directory, "releases", "*", "ocdsadditions_release.json"
            )
        ):
            with (open(path)) as fp:
                data = json.load(fp)
                if data["id"] == release_id:
                    return Release(self, path.split("/")[-2])
        raise Exception("Release does not exist")

    def get_extensions_used(self):
        extensions = []
        for release in self.list_releases():
            package_data = release.get_package_data()
            if "extensions" in package_data and isinstance(
                package_data["extensions"], list
            ):
                extensions.extend(package_data["extensions"])
        return sorted(list(set(extensions)))

    def write_record_package(self, filename):

        releases = [r.get_release_package() for r in self.list_releases()]

        latest_version_releases: list = []
        for release in releases:
            if ocdskit.util.get_ocds_minor_version(release) == "1.0":
                upgraded = ocdskit.upgrade.upgrade_10_11(
                    json.loads(json.dumps(release), object_pairs_hook=OrderedDict)
                )
                latest_version_releases.append(json.loads(json.dumps(upgraded)))
            else:
                latest_version_releases.append(release)

        generator = ocdskit.combine.merge(
            latest_version_releases,
            return_package=True,
        )
        data = next(generator)
        with open(filename, "w") as fp:
            json.dump(data, fp, indent=4)


class Release:
    def __init__(self, contracting_process: ContractingProcess, directory_name: str):
        self._contracting_process = contracting_process
        self._directory_name = directory_name

        self._release_directory = os.path.join(
            contracting_process._ocid_directory, "releases", directory_name
        )
        if not os.path.isdir(self._release_directory):
            raise Exception("Release does not exist")
        if not os.path.isfile(
            os.path.join(self._release_directory, "ocdsadditions_release.json")
        ):
            raise Exception("Release file not found")

    def get_id(self):
        with (open(os.path.join(self._release_directory, "release.json"))) as fp:
            data: dict = json.load(fp)
        return data.get("id")

    def set_release_data(self, release_data: dict):
        with open(os.path.join(self._release_directory, "release.json"), "w") as fp:
            json.dump(release_data, fp, indent=4)

    def get_release_package(self) -> dict:
        with (
            open(os.path.join(self._release_directory, "ocdsadditions_release.json"))
        ) as fp:
            meta = json.load(fp)
        with (open(os.path.join(self._release_directory, "package.json"))) as fp:
            data = json.load(fp)
        with (open(os.path.join(self._release_directory, "release.json"))) as fp:
            data["releases"] = [json.load(fp)]
        if meta.get("url"):
            # This indicates the releases was "stolen" from elswehere. We should add a "rel" link.
            # These links will become standard in OCDS 1.2, we have been told.
            if not "links" in data["releases"][0]:
                data["releases"][0]["links"] = []
            if not isinstance(data["releases"][0]["links"], list):
                raise Exception("Releases Links section is not a list")
            data["releases"][0]["links"].append(
                {"rel": "canonical", "href": meta["url"]}
            )
        return data

    def write_release_package(self, filename):
        with open(filename, "w") as fp:
            json.dump(self.get_release_package(), fp, indent=4)

    def create_spreadsheet(self, spreadsheet_filename: str):
        # Make sure filename & type is valid
        output_format: str = ""
        if spreadsheet_filename.endswith(".xlsx"):
            output_format = "xlsx"
        elif spreadsheet_filename.endswith(".ods"):
            output_format = "ods"
        else:
            raise Exception("Unknown output type")

        # Make Schema
        with (open(os.path.join(self._release_directory, "package.json"))) as fp:
            package_data = json.load(fp)
        builder = ProfileBuilder(
            get_ocds_patch_tag(package_data.get("version", "1.0")),
            package_data.get("extensions", []),
        )
        schema = builder.patched_release_schema()
        schema_temp_file = tempfile.mkstemp(suffix=".json", prefix="ocds-additions")
        os.close(schema_temp_file[0])
        with open(schema_temp_file[1], "w") as fp:
            json.dump(schema, fp, indent=4)

        # Make release package
        rel_package_temp_file = tempfile.mkstemp(
            suffix=".json", prefix="ocds-additions"
        )
        os.close(rel_package_temp_file[0])
        self.write_release_package(rel_package_temp_file[1])

        # Create!
        flatten(
            rel_package_temp_file[1],
            schema=schema_temp_file[1],
            output_format=output_format,
            output_name=spreadsheet_filename,
            root_id="ocid",
            main_sheet_name="releases",
            root_list_path="releases",
        )

        # Remove temp file
        os.unlink(rel_package_temp_file[1])
        os.unlink(schema_temp_file[1])

    def get_release_data_filename(self) -> str:
        return os.path.join(self._release_directory, "release.json")

    def get_release_data(self) -> dict:
        with open(self.get_release_data_filename()) as fp:
            return json.load(fp)

    def get_package_data_filename(self) -> str:
        return os.path.join(self._release_directory, "package.json")

    def get_package_data(self) -> dict:
        with open(self.get_package_data_filename()) as fp:
            return json.load(fp)

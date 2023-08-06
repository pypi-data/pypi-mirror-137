import platform
import sys
from argparse import ArgumentParser, Namespace
from glob import glob
from os.path import dirname, exists, isdir, join
from typing import List, Optional

import sila2.code_generator
from sila2.code_generator.code_generator import CodeGenerator
from sila2.code_generator.feature_generator import FeatureGenerator
from sila2.framework import Feature


def _get_feature_definition_paths(feature_definition_paths: List[str]) -> List[str]:
    if platform.system() != "Windows":
        return feature_definition_paths

    paths = []
    for path in feature_definition_paths:
        files = glob(path, recursive=True)
        if not files:
            raise FileNotFoundError(f"No such files: '{path}'")
        paths.extend(files)
    return paths


def package(args: Namespace) -> None:
    package_name: str = args.package_name
    out_dir: str = args.output_dir
    overwrite: bool = args.overwrite
    feature_definitions: List[str] = _get_feature_definition_paths(args.feature_definitions)
    lock_controller: bool = args.lock_controller
    auth_features: bool = args.auth_features
    for_git_repo: bool = args.git

    features = [Feature(open(fdl_file).read()) for fdl_file in sorted(feature_definitions)]
    generator = CodeGenerator(overwrite=overwrite)
    generator.generate_package(
        package_name,
        features,
        out_dir,
        lock_controller=lock_controller,
        auth_features=auth_features,
        for_git_repo=for_git_repo,
    )
    generator.format_generated_files()


def add_features(args: Namespace) -> None:
    package_dir: str = args.package_dir
    new_fdl_files: List[str] = _get_feature_definition_paths(args.feature_definitions)

    if not exists(join(package_dir, "setup.py")):
        print("Given directory is not a package (does not contain setup.py)", file=sys.stderr)
        return

    generated_dir = find_matching_directory(join(package_dir, "*", "generated"))
    implementation_dir = find_matching_directory(join(package_dir, "*", "feature_implementations"))

    existing_fdl_files = glob(join(generated_dir, "*", "*.sila.xml"))

    old_features = {}
    for fdl_file in existing_fdl_files:
        feature = Feature(open(fdl_file).read())
        old_features[feature._identifier] = feature

    new_features = {}
    for fdl_file in new_fdl_files:
        feature = Feature(open(fdl_file).read())
        if feature._identifier in old_features:
            raise ValueError(f"Feature {feature._identifier} already exists. Use 'update' instead.")
        new_features[feature._identifier] = feature

    features = list(old_features.values()) + list(new_features.values())
    features.sort(key=lambda f: f._identifier)

    generator = CodeGenerator(overwrite=True)
    generator.generate_generated_dir(features, generated_dir)
    generator.generate_implementations(list(new_features.values()), implementation_dir)
    generator.format_generated_files()


def update(args: Namespace) -> None:
    package_dir: str = args.package_dir

    generated_dir = find_matching_directory(join(package_dir, "*", "generated"))
    implementation_dir = find_matching_directory(join(package_dir, "*", "feature_implementations"))

    features = []
    generator = CodeGenerator(overwrite=True)
    for fdl_file in sorted(glob(join(generated_dir, "*", "*.sila.xml"))):
        feature = Feature(open(fdl_file).read())
        feature_generator = FeatureGenerator(feature, overwrite=True)
        features.append(feature)

        feature_dir = dirname(fdl_file)
        old_base = open(f"{feature_dir}/{feature._identifier.lower()}_base.py").read()

        feature_generator.generate_feature_files(feature_dir)
        new_base = open(f"{feature_dir}/{feature._identifier.lower()}_base.py").read()

        # if base class changed: generate new impl
        if old_base != new_base:
            feature_generator.generate_impl(implementation_dir, prefix="updated_")
        generator.generated_files.extend(feature_generator.generated_files)
    generator._generate_client(features, generated_dir)
    generator.format_generated_files()


def find_matching_directory(pattern: str) -> str:
    matches = glob(pattern)
    if not matches:
        raise ValueError(f"No matching directory found: {pattern}")
    if len(matches) > 1:
        raise ValueError(f"Multiple matches found: {pattern}")

    match = matches[0]
    if not isdir(match):
        raise NotADirectoryError(f"Not a directory: {match}")
    return match


def main(argv: Optional[List[str]] = None) -> int:
    parser = ArgumentParser(
        prog=sila2.code_generator.__name__,
        description="SiLA 2 Python Code Generator",
    )
    parser.add_argument("--debug", action="store_true", help="Display more detailed error messages")
    commands = parser.add_subparsers(title="Commands", required=True, dest="command")

    # package generation subparser
    package_parser = commands.add_parser(
        "new-package", description="Generate a SiLA 2 Server/Client Python package from given feature definitions"
    )
    package_parser.add_argument("-n", "--package-name", help="Package name", required=True)
    package_parser.add_argument("-o", "--output-dir", default=".", help="Package directory (will contain 'setup.py')")
    package_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    package_parser.add_argument("--git", action="store_true", help="Generate .gitignore and README.md")
    package_parser.add_argument(
        "--lock-controller", action="store_true", help="Add default implementation of the core feature LockController"
    )
    package_parser.add_argument(
        "--auth-features",
        action="store_true",
        help="Add default implementations of the core features "
        "AuthenticationService, AuthorizationProviderService and AuthorizationService",
    )
    package_parser.add_argument("feature_definitions", nargs="*", help="SiLA 2 feature definitions")
    package_parser.set_defaults(func=package)

    # feature addition subparser
    add_features_parser = commands.add_parser(
        "add-features", description="Add features to previously generated package"
    )
    add_features_parser.add_argument("-d", "--package-dir", default=".", help="Package directory (contains 'setup.py')")
    add_features_parser.add_argument("feature_definitions", nargs="*", help="SiLA 2 feature definitions")
    add_features_parser.set_defaults(func=add_features)

    # package update subparser
    update_parser = commands.add_parser(
        "update",
        description="Update a previously generated package after modifications to the feature definitions "
        "(refreshes the 'generated' submodule)",
    )
    update_parser.add_argument("-d", "--package-dir", default=".", help="Package directory (contains 'setup.py')")
    update_parser.set_defaults(func=update)

    args = parser.parse_args(argv)

    try:
        args.func(args)
        return 0
    except Exception as ex:
        if args.debug:
            raise ex

        print(f"{ex.__class__.__name__}: {ex}", file=sys.stderr)
        return 1

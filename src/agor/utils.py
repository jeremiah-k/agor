import hashlib
import os
import shutil
import tarfile
import zipfile
from pathlib import Path
from typing import Optional

import httpx
from tqdm import tqdm

from .constants import (
    DOWNLOAD_CHUNK_SIZE,
    PROGRESS_BAR_WIDTH,
    SUPPORTED_COMPRESSION_FORMATS,
)
from .exceptions import CompressionError, NetworkError
from .settings import settings


def move_directory(src_dir: Path, dest_dir: Path):
    dest_dir.mkdir(
        parents=True, exist_ok=True
    )  # Ensures that the destination directory exists

    for item in src_dir.iterdir():
        shutil.move(str(item), str(dest_dir))

    return dest_dir


def download_file(
    url: str, dest_path: Path, expected_sha256: Optional[str] = None
) -> Path:
    """
    Download a file from URL with progress bar and optional integrity checking.

    Args:
        url: URL to download from
        dest_path: Path to save the downloaded file
        expected_sha256: Optional SHA256 hash for integrity verification

    Returns:
        Path to the downloaded file

    Raises:
        NetworkError: If download fails
        CompressionError: If integrity check fails
    """
    try:
        with httpx.stream("GET", url, follow_redirects=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))

            t = tqdm(
                desc="📥 Downloading git binary",
                total=total_size,
                unit="iB",
                unit_scale=True,
                ncols=PROGRESS_BAR_WIDTH,
            )

            sha256_hash = hashlib.sha256() if expected_sha256 else None

            with open(dest_path, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=DOWNLOAD_CHUNK_SIZE):
                    t.update(len(chunk))
                    f.write(chunk)
                    if sha256_hash:
                        sha256_hash.update(chunk)
            t.close()

            if total_size != 0 and t.n != total_size:
                raise NetworkError(
                    f"Download incomplete: expected {total_size} bytes, got {t.n}"
                )

            # Verify integrity if expected hash provided
            if expected_sha256 and sha256_hash:
                actual_hash = sha256_hash.hexdigest()
                if actual_hash != expected_sha256:
                    dest_path.unlink(missing_ok=True)  # Remove corrupted file
                    raise CompressionError(
                        f"File integrity check failed. Expected: {expected_sha256}, got: {actual_hash}"
                    )

    except httpx.HTTPError as e:
        raise NetworkError(f"Failed to download {url}: {e}") from e
    except OSError as e:
        raise NetworkError(f"Failed to save file to {dest_path}: {e}") from e

    return dest_path


def create_archive(
    dir_to_compress: Path,
    archive_path: Path,
    compression: str = None,
) -> Path:
    """
    Create an archive (ZIP or TAR) from a directory.

    Args:
        dir_to_compress: Directory to compress
        archive_path: Path for the output archive
        compression: Compression format ('zip', 'gz', 'bz2')

    Returns:
        Path to the created archive

    Raises:
        CompressionError: If compression fails
        ValueError: If compression format is invalid
    """
    # Use default compression format if none provided
    if compression is None:
        compression = settings.compression_format

    # Ensure the directory exists
    if not dir_to_compress.exists() or not dir_to_compress.is_dir():
        raise CompressionError(f"'{dir_to_compress}' is not a valid directory.")

    # Validate compression type
    if compression not in SUPPORTED_COMPRESSION_FORMATS:
        raise ValueError(
            f"Invalid compression type: {compression}. "
            f"Supported formats: {', '.join(SUPPORTED_COMPRESSION_FORMATS)}"
        )

    # Get the total number of files to compress for progress reporting
    total_files = sum(len(files) for _, _, files in os.walk(dir_to_compress))

    try:
        if compression == "zip":
            return _create_zip_archive(dir_to_compress, archive_path, total_files)
        else:
            return _create_tar_archive(
                dir_to_compress, archive_path, compression, total_files
            )
    except Exception as e:
        raise CompressionError(f"Failed to create archive: {e}") from e


def _create_zip_archive(
    dir_to_compress: Path, archive_path: Path, total_files: int
) -> Path:
    """Create a ZIP archive."""
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        with tqdm(
            total=total_files,
            desc="📦 Creating ZIP archive",
            ncols=PROGRESS_BAR_WIDTH,
            unit="file",
        ) as pbar:
            for root, _dirs, files in os.walk(dir_to_compress):
                for file in files:
                    absolute_file_path = os.path.join(root, file)
                    relative_file_path = os.path.relpath(
                        absolute_file_path, dir_to_compress
                    )
                    zipf.write(absolute_file_path, arcname=relative_file_path)
                    pbar.update()
    return archive_path


def _create_tar_archive(
    dir_to_compress: Path, archive_path: Path, compression: str, total_files: int
) -> Path:
    """Create a TAR archive with specified compression."""
    with tarfile.open(archive_path, f"w:{compression}") as tar:
        with tqdm(
            total=total_files,
            desc=f"📦 Creating TAR.{compression.upper()} archive",
            ncols=PROGRESS_BAR_WIDTH,
            unit="file",
        ) as pbar:
            for root, _dirs, files in os.walk(dir_to_compress):
                for file in files:
                    absolute_file_path = os.path.join(root, file)
                    relative_file_path = os.path.relpath(
                        absolute_file_path, dir_to_compress
                    )
                    tar.add(absolute_file_path, arcname=relative_file_path)
                    pbar.update()
    return archive_path


# Backward compatibility alias
def create_tarball(dir_to_tar: Path, tar_file_path: Path, compression="gz") -> Path:
    """Legacy function for backward compatibility."""
    return create_archive(dir_to_tar, tar_file_path, compression)


def move_file(src_file: Path, dest_dir: Path) -> Path:
    destination = dest_dir / src_file.name
    shutil.move(str(src_file), str(destination))
    return destination

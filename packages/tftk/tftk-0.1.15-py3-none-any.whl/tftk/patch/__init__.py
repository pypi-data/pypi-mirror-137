import platform

__all__ = []

if platform.system() == 'Windows':
    from . tensorflow_datasets_issue_35630 import ENABLE_PATCH_TFDS_35630
    ENABLE_PATCH_TFDS_35630()

__all__.append(
    'ENABLE_PATCH_TFDS_35630'
)
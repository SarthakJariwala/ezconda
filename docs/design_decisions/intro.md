# Introduction

**EZconda** takes the approach of keeping two files for managing `conda` environments.

1. **[Specifications file](specfile.md)** contains the packages and channels (and *only those* packages/channels) that the [user requests via the command line](../user_guide/install_packages.md).

2. **[Lock file](lockfile.md)** contains _**all**_ the packages along with the *exact version and build number and channels*. It also contains other metadata such as the system information where it was generated, etc.


> The two files keep environments and corresponding specifications in sync as well as [support reproducible environment creation](../user_guide/recreate_env.md).
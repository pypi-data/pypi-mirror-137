With Cluster on Demand for VMware you can spin up a cluster running Bright
Cluster Manager on VMware vSphere.

# Installation

```
pip install cm-cluster-on-demand-vmware
```

# Usage

To get started, execute the following command:

```
cm-cod-vmware --help
```

Example, To start a Bright Cluster with 5 nodes and 1 headnode on vSphere:

```
cm-cod-vmware cluster create --on-error 'cleanup' --wlm 'slurm' --nodes '5' --externalnet-vdportgroup '...' --vdswitch--name '...'  --cluster-password '...'  --license-product-key '...' --name mycluster
```

Don't forget to fill in the '...' blanks, and change the other parameters to
the values that match your use-case and organization. To obtain a Bright
product key, please contact sales@brightcomputing.com. All documentation for
setting up and running a Bright cluster using Cluster On Demand on vSphere can
be found in the
[Cloudbursting Manual](https://www.brightcomputing.com/documentation).


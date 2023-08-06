With Cluster on Demand for Azure you can spin up a cluster running Bright
Cluster Manager inside of Azure.

# Installation

```
pip install cm-cluster-on-demand-azure
```

# Usage

To get started, execute the following command:

```
cm-cod-azure --help
```

Example, To start a Bright Cluster with 5 nodes and 1 headnode in Azure:

```
cm-cod-azure cluster create --on-error 'cleanup' $REGION$' --wlm 'slurm' --nodes '5' $AZURE CREDENTIALS$ --cluster-password '...'  --license-product-key '...' --name mycluster
```

Don't forget to fill in the '...' blanks, and change the other parameters to
the values that match your use-case and organization. To obtain a Bright
product key, please contact sales@brightcomputing.com. All documentation for
setting up and running a Bright cluster using Cluster On Demand on Azure can be
found in the
[Cloudbursting Manual](https://www.brightcomputing.com/documentation).

If you have an account in Bright Computing's Customer Portal, you can also
create a AWS/Azure cluster from there.

# This playbook

This playbook was designed for simplicity and is intended for use in a test environment only. 
It is only capable of interacting with Debian based Linux machines and was tested with Ubuntu instances.

## Pre flight configuration
To execute this playbook, you will need to make sure you have key-based ssh access to all of your instances. Use the same key for all of them, and save your private key in the playbook folder.
You will also need to configure one user (The same user in all of them) with passwordless root access in all of the instances. 

**Obs.** If deploying in AWS EC2, for example, the requirements above are fulfilled automatically by choosing the key-based access during deployment. 

## hosts-inventory
This playbook is based on **ceph_deploy**. As such, ansible will only interact with one instance: The bootstrap instance.
Set the address of this instance, name of the key file and ssh user in the *hosts-inventory* file, following the pattern:

```
`your_bootstrap_host_address ansible_ssh_private_key_file=./your_file ansible_user=ubuntu`
```
When executing the playbook, remember to add the -i parameter, pointing to the file hosts-inventory

## variables.yml

In this file, you will need to specify the responsibilities of each instance, as well as the drives that will be used by Ceph and some additional configurations.
Ceph will use entire drives or partitions, and these shouldn't be mounted at the beginning of the installation.
If you already partitioned your drive, make sure to uncomment the tasks designed for this use-case, in the file playbook.yml

More details about the configuration process can be found in the file itself.

## Creating a user

After the deployment is finished, log-in to the rgw_host and create a user executing the command

```
radosgw-admin user create --uid="{user-name}" --display-name="{Display Name}"
```
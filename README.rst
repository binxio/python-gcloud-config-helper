====================
gcloud config helper
====================
This library allows you to use the current gcloud configuration credentials to authenticate with against
the google APIs.

The library provides the class GCloudCredentials which wraps the `gcloud config config-helper` command.

To use::

    import gcloud_config_helper
    credentials, project = gcloud_config_helper.default()

Next you can pass these credentials in when constructing an API client::

    from google.cloud import compute_v1
    c = compute_v1.InstancesClient(credentials=credentials)
    for zone, instances in c.aggregated_list(request={"project": project}):
	for instance in instances.instances:
	    print(f'found {instance.name} in zone {zone}')

Note that Google documentation states that `gcloud config config-helper` should be regarded as an
unstable interface.

if you want, you can use the `gcloud_config_helper.on_path()` to determine to use gcloud or the
default credentials::

    if google_config_helper.on_path():
       credentials, project = gcloud_config_helper.default()
    else:
       logging.info("using application default credentials")
       credentials, project = google.auth.default()


.. image:: https://img.shields.io/pypi/v/gcloud_config_helper.svg
        :target: https://pypi.python.org/pypi/gcloud_config_helper

.. image:: https://img.shields.io/travis/binxio/python-gcloud-config-helper.svg
        :target: https://travis-ci.com/binxio/python-gcloud-config-helper

.. image:: https://readthedocs.org/projects/gcloud-config-helper/badge/?version=latest
        :target: https://gcloud-config-helper.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



obtain Google gcloud configuration credentials


* Free software: Apache Software License 2.0

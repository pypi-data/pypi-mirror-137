# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bods_client', 'bods_client.models']

package_data = \
{'': ['*']}

install_requires = \
['gtfs-realtime-bindings>=0.0.7,<0.0.8',
 'lxml>=4.7.1,<5.0.0',
 'pydantic>=1.8,<1.9',
 'python-dateutil>=2.8,<2.9',
 'requests>=2.25,<2.26',
 'urllib3>=1.26,<1.27']

setup_kwargs = {
    'name': 'bods-client',
    'version': '0.7.1',
    'description': 'A Python client for the Department for Transport Bus Open Data Service API',
    'long_description': '# bods-client\n\n[![Build Status](https://github.com/ciaranmccormick/python-bods-client/workflows/test/badge.svg?branch=main&event=push)](https://github.com/ciaranmccormick/python-bods-client/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/ciaranmccormick/python-bods-client/branch/main/graph/badge.svg)](https://codecov.io/gh/ciaranmccormick/python-bods-client)\n[![Python Version](https://img.shields.io/pypi/pyversions/bods-client.svg)](https://pypi.org/project/bods-client/)\n\nA Python client for the Department for Transport Bus Open Data Service API\n\n\n## Installation\n\n```bash\npip install bods-client\n```\n\n\n## Example\n\n\n### GTFS RT\n\nAll the vehicle locations for vehicles in a geographical location can be obtained\nusing the `get_gtfs_rt_data_feed` method with a boundng box.\n\n```python\n\nfrom bods_client.client import BODSClient\nfrom bods_client.models import BoundingBox, GTFSRTParams\n\n# An API key can be obtained by registering with the Bus Open Data Service\n# https://data.bus-data.dft.gov.uk/account/signup/\n>> API_KEY = "api-key"\n\n>> bods = BODSClient(api_key=API_KEY)\n>> bounding_box = BoundingBox(\n    **{\n        "min_latitude": 51.26,\n        "max_latitude": 51.75,\n        "min_longitude": -0.54,\n        "max_longitude": 0.27,\n    }\n)\n>> params = GTFSRTParams(bounding_box=bounding_box)\n>> message = bods.get_gtfs_rt_data_feed(params=params)\n>> message.entity[0]\nid: "421354378097713049"\nvehicle {\n  trip {\n    trip_id: ""\n    route_id: ""\n  }\n  position {\n    latitude: 51.712860107421875\n    longitude: -0.38401100039482117\n    bearing: 170.0\n  }\n  timestamp: 1614396229\n  vehicle {\n    id: "7214"\n  }\n}\n\n```\n\nThis returns a `google.transit.gtfs_realtime_pb2.FeedMessage` object. More details about\nGeneral Transit Feed Specification Realtime Transit (GTFS-RT) can be found\n[here](https://developers.google.com/transit/gtfs-realtime/).\n\n\n### SIRI VM\n\nVehicle locations are also provided in the SIRI-VM XML format using the\n`get_siri_vm_data_feed` method. The data can then parsed using an xml\nparser library such as `lxml`.\n\n```python\nfrom bods_client.client import BODSClient\nfrom bods_client.models import BoundingBox, Siri, SIRIVMParams\n\n\n>> API_KEY = "api-key"\n\n>> client = BODSClient(api_key=API_KEY)\n>> bounding_box = BoundingBox(\n    **{\n        "min_latitude": 51.267729,\n        "max_latitude": 51.283191,\n        "min_longitude": -0.142423,\n        "max_longitude": 0.177432,\n    }\n)\n\n>> params = SIRIVMParams(bounding_box=bounding_box)\n>> siri_response = client.get_siri_vm_data_feed(params=params)\n>> siri = Siri.from_bytes(siri_response)\n>> siri.service_delivery.vehicle_monitoring_delivery.vehicle_activities[0]\nVehicleActivity(\n    recorded_at_time=datetime.datetime(\n        2022, 1, 31, 19, 48, 24, tzinfo=datetime.timezone.utc\n    ),\n    item_identifier="05fc46f3-9629-4336-9a8d-f397030f5891",\n    valid_until_time=datetime.datetime(2022, 1, 31, 21, 5, 21, 997139),\n    monitored_vehicle_journey=MonitoredVehicleJourney(\n        bearing=135.0,\n        block_ref=None,\n        framed_vehicle_journey_ref=None,\n        vehicle_journey_ref="447183",\n        destination_name="BEDDINGTON (ABELLIO LONDON)",\n        destination_ref=None,\n        orgin_name=None,\n        origin_ref="40004410084D",\n        origin_aimed_departure_time=datetime.datetime(\n            2022, 1, 31, 19, 53, tzinfo=datetime.timezone.utc\n        ),\n        direction_ref="1",\n        published_line_name="407",\n        line_ref="296",\n        vehicle_location=VehicleLocation(longitude=-0.077464, latitude=51.282658),\n        operator_ref="TFLO",\n        vehicle_ref="16085",\n    ),\n)\n```\n\nDetails about the SIRI specification can be found [here](http://www.transmodel-cen.eu/standards/siri/).\n\n\n## License\n\n[MIT](https://github.com/ciaran.mccormick/bods-client/blob/master/LICENSE)\n',
    'author': 'Ciaran McCormick',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ciaranmccormick/python-bods-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

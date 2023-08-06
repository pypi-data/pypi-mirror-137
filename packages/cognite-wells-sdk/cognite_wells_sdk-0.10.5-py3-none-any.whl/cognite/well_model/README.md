# Installation with pip

```bash
pip install cognite-wells-sdk
```

# Usage

## Authenticating and creating a client

### With environment variables

**NOTE**: *must be valid for both cdf and geospatial API*

```bash
export COGNITE_PROJECT=<project-tenant>
export COGNITE_API_KEY=<your-api-key>
```

You can then initialize the client with
```py
from cognite.well_model import CogniteWellsClient
wells_client = CogniteWellsClient()
```

### Without environment variables

Alternatively, the client can be initialized like this:

```python
import os
from cognite.well_model import CogniteWellsClient
api_key = os.environ["COGNITE_API_KEY"]
wells_client = CogniteWellsClient(project="your-project", api_key=api_key)
```

## **Well queries**

#### Get well by asset external id or matching id

```python

well: Well = client.wells.retrieve(asset_external_id="VOLVE:15/9-F-15")

# OR specify matching_id

well: Well = client.wells.retrieve(matching_id="kfe72ik")
```

#### Get multiple wells by asset external ids or matching ids

```python
wells = client.wells.retrieve_multiple(
    asset_external_ids=["VOLVE:15/9-F-15"],
    matching_ids=["je93kmf"]
)
```


#### Delete well

Warning! Note that if you delete a _well_, it will cascade to delete all _wellbores_, _measurements_, _trajectories_,
_NPT events_, and _NDS events_ connected to that well asset.

```python
to_delete: List[AssetSource] = [AssetSource(asset_external_id="VOLVE:15/9-F-15", source_name="VOLVE")]
client.wells.delete(to_delete)
```

#### List wells

```python
wells = wells_client.wells.list()
```

#### Filter wells by wkt polygon

```python
from cognite.well_model.models import PolygonFilter

polygon = 'POLYGON ((0.0 0.0, 0.0 80.0, 80.0 80.0, 80.0 0.0, 0.0 0.0))'
wells = wells_client.wells.filter(polygon=PolygonFilter(geometry=polygon, crs="epsg:4326"))
```

#### Filter wells by wkt polygon, name/description and specify desired outputCrs

```python
polygon = 'POLYGON ((0.0 0.0, 0.0 80.0, 80.0 80.0, 80.0 0.0, 0.0 0.0))'
wells = wells_client.wells.filter(
    polygon=PolygonFilter(geometry=polygon, crs="epsg:4326", geometry_type="WKT"),
    string_matching="16/",
    output_crs="EPSG:23031"
)
```

#### Get wells that have a trajectory

```python
from cognite.well_model.models import TrajectoryFilter

wells = wells_client.wells.filter(trajectories=TrajectoryFilter(), limit=None)
```

#### Get wells that have a trajectory with data between certain depths

```python
wells = wells_client.wells.filter(trajectories=TrajectoryFilter(min_depth=1400.0, max_depth=1500.0), limit=None)
```

#### Get wells that has the right set of measurement types

```python
from cognite.well_model.models import MeasurementFilter, MeasurementFilters, MeasurementType

gammarayFilter = MeasurementFilter(measurement_type=MeasurementType.gamma_ray)
densityFilter = MeasurementFilter(measurement_type=MeasurementType.density)

# Get wells with all measurements
measurements_filter = MeasurementFilters(contains_all=[gammarayFilter, densityFilter])
wells = wells_client.wells.filter(measurements=measurements_filter, limit=None)

# Or get wells with any of the measurements
measurements_filter = MeasurementFilters(contains_any=[gammarayFilter, densityFilter])
wells = wells_client.wells.filter(measurements=measurements_filter, limit=None)
```

#### Get wells that has right set of npt event criterias
```python
npt = WellNptFilter(
    duration=DoubleRange(min=1.0, max=30.0),
    measuredDepth=LengthRange(min=1800.0, max=3000.0, unit=DistanceUnitEnum.meter),
    nptCodes=ContainsAllOrAny(containsAll=["FJSB", "GSLB"]),
    nptCodeDetails=ContainsAllOrAny(containsAll=["SLSN", "OLSF"]),
)

well_items = client.wells.filter(npt=npt)
```

## **Wellbore queries**

#### Get wellbore by asset external id or matching id

```python
wellbore: Wellbore = client.wellbores.retrieve(asset_external_id="VOLVE:15/9-F-15 A")

# OR specify a matching_id

wellbore: Wellbore = client.wellbores.retrieve(matching_id="32bc81ce")
```

#### Get multiple wellbores by asset external ids or matching ids

```python
wellbore_items = client.wellbores.retrieve_multiple(
    asset_external_ids=["VOLVE:15/9-F-15 B", "VOLVE:15/9-F-15 C", "VOLVE:15/9-F-4", "VOLVE:13/10-F-11 T2"],
    matching_ids=["2984nfe", "nfy39g", "jkey73g"]
)
```

#### Get wellbores from a single well by asset external id or matching id

```python
wellbore_items = client.wellbores.retrieve_multiple_by_well(asset_external_id="VOLVE: WELL-202")

# OR specify matching_id

wellbore_items = client.wellbores.retrieve_multiple_by_well(matching_id="fok8240f")
```

## **Trajectory queries**

#### Get trajectories by wellbore asset external id or matching id

```python
trajectory_list = client.trajectories.retrieve_multiple_by_wellbore(
    asset_external_id="VOLVE: WELLBORE-202"
)

# OR specify matching id

trajectory_list = client.trajectories.retrieve_multiple_by_wellbore(
    matching_id="ko73kf"
)
```

#### Get trajectories by wellbore asset external ids or matching ids

```python
trajectory_list = client.trajectories.retrieve_multiple_by_wellbores(
    asset_external_ids=["VOLVE: WELLBORE-201", "VOLVE: WELLBORE-202"],
    matching_ids=["kfe7kf", "kie832"]
)
```

#### List trajectory data

```python
request = TrajectoryDataRequest(
    sequence_external_id="13/10-F-11 T2 ACTUAL",
    measured_depth_range=DepthRange(min_depth=2, max_depth=5, unit="meter"),
    true_vertical_depth_range=DepthRange(min_depth=0.2, max_depth=0.5, unit="meter"),
)
trajectories = client.trajectories.list_data([request])
```

## **Measurement queries**

#### Get multiple measurements from wellbore asset external id or matching id
```py
measurement_list = client.measurements.retrieve_multiple_by_wellbore(asset_external_id="VOLVE:WELLBORE-201")

# OR specify matching_id
measurement_list = client.measurements.retrieve_multiple_by_wellbore(matching_id="9u2jnf")
```

#### Get multiple measurements from wellbore asset external ids or matching ids
```py
valid_wellbore_ids = ["VOLVE:WELLBORE-201", "VOLVE:WELLBORE-202"]
measurement_list = client.measurements.retrieve_multiple_by_wellbores(asset_external_ids=valid_wellbore_ids)
```

#### Filter measurement data
```py
measurement_data_request = MeasurementDataRequest(
        sequence_external_id="VOLVE:seq1",
        measured_depth_range=DepthRange(min_depth=0.0, max_depth=10_000.0, unit="meter"),
    )

measurement_data_list: MeasurementDataList = client.measurements.list_data([measurement_data_request])
```

## **NPT Event queries**

#### Filter NPT events
```py
npt_events = client.npt.list(
    duration=DoubleRange(min=3.0, max=10.5),
    md=LengthRange(min=590.0, max=984.0, unit="meter"),
    npt_codes=["O"],
    npt_code_details=["1KFO"],
    wellbore_asset_external_ids=["VOLVE:15/9-F-15 A", "VOLVE:15/9-F-15 D"],
    wellbore_matching_ids=["KFOEFW"]
)
```

#### List all NPT codes
```py
npt_codes: List[str] = client.npt.codes()
```

#### List all NPT detail codes
```py
npt_detail_codes: List[str] = client.npt.detail_codes()
```

## **NDS Event queries**

#### Filter NDS events
```py
nds_events = client.nds.list(
    hole_start=LengthRange(min=10, max=15, unit="meter"),
    hole_end=LengthRange(min=20, max=35, unit="meter"),
    wellbore_asset_external_ids=["VOLVE:15/9-F-15 A"],
    wellbore_matching_ids=["KOEFKE"],
    probabilities=[3, 5],
    severities=[3, 5]
)
```

#### List all NDS risk types
```py
risk_types: List[str] = client.nds.risk_types()
```

## Casing queries

#### Filter casings
```py
casings = client.casings.list(
    wellbore_asset_external_ids=["VOLVE:15/9-F-15 A"],
    wellbore_matching_ids=["KOEFKE"],
)
```

## Ingestion

### Initialise tenant

Before ingesting any wells, the tenant must be initialized to add in the standard assets and labels used in the WDL.

```python
from cognite.well_model import CogniteWellsClient

wells_client = CogniteWellsClient()
log_output = wells_client.ingestion.ingestion_init()
print(log_output)  # If something is wrong with authorization, you should see that in the logs
```

### Add source

Before ingestion from a source can take place, the source must be registered in WDL.

```python
import os
from cognite.well_model import CogniteWellsClient

wells_client = CogniteWellsClient()
created_sources = wells_client.sources.ingest_sources(["Source1, Source2"])
```

### Ingest wells
```python
import os
from datetime import date

from cognite.well_model import CogniteWellsClient
from cognite.well_model.models import DoubleWithUnit, WellDatum, Wellhead, WellIngestion

wells_client = CogniteWellsClient()
source_asset_id = 102948135620745 # Id of the well source asset in cdf

well_to_create = WellIngestion(
    asset_id=source_asset_id,
    well_name="well-name",
    description="Optional description for the well",
    country="Norway",
    quadrant="25",
    block="25/5",
    field="Example",
    operator="Operator1",
    spud_date=date(2021, 3, 17),
    water_depth=0.0,
    water_depth_unit="meters",
    wellhead=Wellhead(
        x = 21.0,
        y = 42.0,
        crs = "EPSG:4236" # Must be a EPSG code
    ),
    datum=WellDatum(
        elevation = DoubleWithUnit(value=1.0, unit="meters"),
        reference = "well-datum-reference",
        name = "well-datum-name"
    ),
    source="Source System Name"
)

wells_client.ingestion.ingest_wells([well_to_create]) # Can add multiple WellIngestion objects at once
```

### Ingest wellbores with optional well and/or trajectory
```python
import os

from cognite.well_model import CogniteWellsClient
from cognite.well_model.models import (
    DoubleArrayWithUnit,
    TrajectoryIngestion,
    WellIngestion,
    WellboreIngestion,
    ParentType,
    MeasurementIngestion,
    MeasurementField,
    MeasurementType
)

wells_client = CogniteWellsClient()
source_asset_id = 102948135620745 # Id of the wellbore source asset in cdf
source_trajectory_ext_id = "some sequence ext id" # Id of the source sequence in cdf

well_to_create = WellIngestion(...)
trajectory_to_create = TrajectoryIngestion(
    source_sequence_ext_id=source_trajectory_ext_id,
    measured_depths = DoubleArrayWithUnit(values=[0.0, 1.0, 2.0], unit="meters"),
    inclinations = DoubleArrayWithUnit(values=[10.0, 1.0, 22.0], unit="degrees"),
    azimuths = DoubleArrayWithUnit(values=[80.0, 81.0, 82.0], unit="degrees")
)
measurements_to_create = [
    MeasurementIngestion(
        sequence_external_id="measurement_sequence_1",
        measurement_fields=[
            MeasurementField(type_name=MeasurementType.gamma_ray),
            MeasurementField(type_name=MeasurementType.density),
        ],
    ),
    MeasurementIngestion(
        sequence_external_id="measurement_sequence_2",
        measurement_fields=[
            MeasurementField(type_name=MeasurementType.geomechanics),
            MeasurementField(type_name=MeasurementType.lot),
        ],
    )
]

wellbore_to_create = WellboreIngestion(
    asset_id = source_asset_id,
    wellbore_name = "wellbore name",
    parent_name = "name of parent well or wellbore",
    parent_type = ParentType.well, # or ParentType.wellbore
    well_name = "name of parent well", # top level well; required in addition to the parent name (even if parent is well)
    source = "Source System Name",
    trajectory_ingestion = trajectory_to_create,
    measurement_ingestions = measurements_to_create,
    well_ingestion = well_to_create # if not ingesting a well, then one must already exist
)

wells_client.ingestion.ingest_wellbores([wellbore_to_create]) # Can add multiple WellboreIngestion objects at once
```

### Ingest casing data
```python
import os

from cognite.well_model import CogniteWellsClient
from cognite.well_model.models import (
    CasingAssembly,
    DoubleWithUnit,
    CasingSchematic,
    SequenceSource,
)

client = CogniteWellsClient()

casing_assemblies = CasingAssembly(
    min_inside_diameter=DoubleWithUnit(value=0.1, unit="meter"),
    min_outside_diameter=DoubleWithUnit(value=0.2, unit="meter"),
    max_outside_diameter=DoubleWithUnit(value=0.3, unit="meter"),
    original_measured_depth_top=DoubleWithUnit(value=100, unit="meter"),
    original_measured_depth_base=DoubleWithUnit(value=101, unit="meter"),
)

casing = CasingSchematic(
    wellbore_asset_external_id="VOLVE:wb-1",
    casing_assemblies=casing_assemblies,
    source=SequenceSource(sequence_external_id="VOLVE:seq1", source_name="VOLVE"),
    phase="PLANNED",
)
client.casings.ingest([casing])
```

### Ingest Measurement data

```python
client = CogniteWellsClient()

seq = SequenceMeasurements(
    wellbore_asset_external_id="VOLVE:wb-1",
    source=SequenceSource(sequence_external_id="VOLVE:seq1", source_name="VOLVE"),
    measured_depth=MeasuredDepthColumn(column_external_id="DEPT", unit=DistanceUnit(unit="foot")),
    columns=[
        SequenceMeasurementColumn(measurement_type=MeasurementType.gamma_ray, column_external_id="GR",unit="gAPI"),
        SequenceMeasurementColumn(measurement_type=MeasurementType.resistivity_deep, column_external_id="RDEEP",unit="ohm.m")
    ])

client.measurements.ingest([seq])
```

### Ingest NPT event data
```python
from cognite.well_model import CogniteWellsClient

start_time = 10000000000
end_time = 20000000000

npt_events_to_ingest = [
    NptIngestionItems(
        wellboreName="Platform WB 12.25 in OH",
        wellName="34/10-8",
        npt_items=[
            NptIngestion(
                npt_code="EGSK",
                npt_code_detail="FSK",
                npt_code_level="1",
                source_event_external_id="m2rmB",
                source="EDM-Npt",
                description="REAM OUT TIGHT HOLE",
                start_time=start_time,
                end_time=end_time,
                location="North sea",
                measured_depth=DoubleWithUnit(value=100.0), unit="foot"),
                root_cause=source_event.metadata["root_cause"],
                duration=(end_time - start_time) / (60 * 60 * 1000.0), # in hours
                subtype="GSK"
            )
        ],
    )
]

npt_events = client.ingestion.ingest_npt_events(body)
```

### Ingest NDS event data
```python
from cognite.well_model import CogniteWellsClient

start_time = 10000000000
end_time = 20000000000

nds_events_to_ingest = [
    NdsIngestionItems(
        wellbore_name="Platform WB 12.25 in OH",
        well_name="34/10-8",
        nds_items=[
            NdsIngestion(
                source_event_external_id="nds-source-event",
                source="EDM-Nds",
                hole_start=DoubleWithUnit(value=12358.0, unit="foot"),
                hole_end=DoubleWithUnit(value=15477.0, unit="foot"),
                severity=1,
                probability=1,
                description="npt description",
                hole_diameter=DoubleWithUnit(value=1.25, unit="inches"),
                risk_type="Mechanical",
                subtype="Excessive Drag",
            )
        ],
    )
]

nds_events = client.ingestion.ingest_nds_events(body)
```


# Well structured file extractor

This SDK has a work-in-progress support for the Well Structured File Extractor
(WSFE). The WSFE is a service with a HTTP interface that lets you extract data
from LAS, LIS, ASC, and DLIS files and creates CDF squences from them.

> **NB**: The API
is subject to change, so please make sure you are using the latest version of
the SDK.

## Usage

The arguments for creating a `WellLogExtractorClient` is the same as for
`CogniteWellsClient` and `CogniteClient`. The example below authenticates using
a token.

```py
from cognite.well_model.wsfe.client import WellLogExtractorClient
from cognite.well_model.wsfe.models import CdfFileLocator, CdfSource, Destination, FileType

wsfe = WellLogExtractorClient(
    client_name="test",
    project="subsurface-test",
    cluster="greenfield",
    token="YOUR BEARER TOKEN
)
```

To use the extractor service, you must first upload some DLIS, LAS, ASC, or LIS files to CDF files.
Then you can queue the files like this:

```py
items = [
    CdfFileLocator(
        source=CdfSource(
            file_external_id = "dlis:889",
            file_type=FileType.dlis
        ),
        destination=Destination(datasetExternalId="volve"),
        contains_trajectory = False,
    )
]
status_map = wsfe.submit(items)
```

The `wsfe.submit` call will return a `Dict[str, int]` response. The string is
the external id of the file and the int is a _process id_. To get the current status, you can run:

```py
process_ids = [2145596483]  # or list(status_map.values())
result = wsfe.status(process_ids)
for key, process_state in result.items():
    log = process_state.log
    for seq in process_state.created_sequences:
        print("Created sequence:", seq)
    for event in log.events:
        print(f"{event.timestamp} [{event.severity.value}], {event.message}")
```
Output might look like this:
```
Created sequence: dlis:889:0:0
Created sequence: dlis:889:1:0
2021-10-05 10:34:25.373653 [info], [STARTED] Downloading file from CDF
2021-10-05 10:34:25.584203 [info], [FINISHED] Downloading file from CDF
2021-10-05 10:34:25.584239 [info], [STARTED] Parsing file
2021-10-05 10:34:25.791715 [info], [FINISHED] Parsing file
2021-10-05 10:34:25.792185 [info], [STARTED] Writing 15/9-F-12 to CDF (1/2)
...
```

Created sequences will have metadata `creator:
"well-structured-file-extractor"`.

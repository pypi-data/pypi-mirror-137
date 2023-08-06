# AWS::IoTEvents Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS IoT Events enables you to monitor your equipment or device fleets for
failures or changes in operation, and to trigger actions when such events
occur.

## Installation

Install the module:

```console
$ npm i @aws-cdk/aws-iotevents
```

Import it into your code:

```python
import aws_cdk.aws_iotevents as iotevents
```

## `DetectorModel`

The following example creates an AWS IoT Events detector model to your stack.
The detector model need a reference to at least one AWS IoT Events input.
AWS IoT Events inputs enable the detector to get MQTT payload values from IoT Core rules.

```python
import aws_cdk.aws_iotevents as iotevents


input = iotevents.Input(self, "MyInput",
    input_name="my_input",  # optional
    attribute_json_paths=["payload.deviceId", "payload.temperature"]
)

online_state = iotevents.State(
    state_name="online",
    on_enter=[iotevents.Event(
        event_name="test-event",
        condition=iotevents.Expression.current_input(input)
    )]
)

iotevents.DetectorModel(self, "MyDetectorModel",
    detector_model_name="test-detector-model",  # optional
    description="test-detector-model-description",  # optional property, default is none
    evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
    detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
    initial_state=online_state
)
```

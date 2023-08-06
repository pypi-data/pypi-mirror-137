'''
Datadog-CDK-Constructs supporting AWS CDK V2
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_lambda
import aws_cdk.aws_lambda_nodejs
import aws_cdk.aws_lambda_python_alpha
import aws_cdk.aws_logs
import constructs


class Datadog(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="datadog-cdk-constructs-v2.Datadog",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        add_layers: typing.Optional[builtins.bool] = None,
        api_key: typing.Optional[builtins.str] = None,
        api_key_secret_arn: typing.Optional[builtins.str] = None,
        api_kms_key: typing.Optional[builtins.str] = None,
        capture_lambda_payload: typing.Optional[builtins.bool] = None,
        enable_datadog_logs: typing.Optional[builtins.bool] = None,
        enable_datadog_tracing: typing.Optional[builtins.bool] = None,
        extension_layer_version: typing.Optional[jsii.Number] = None,
        flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
        forwarder_arn: typing.Optional[builtins.str] = None,
        inject_log_context: typing.Optional[builtins.bool] = None,
        log_level: typing.Optional[builtins.str] = None,
        node_layer_version: typing.Optional[jsii.Number] = None,
        python_layer_version: typing.Optional[jsii.Number] = None,
        site: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param add_layers: 
        :param api_key: 
        :param api_key_secret_arn: 
        :param api_kms_key: 
        :param capture_lambda_payload: 
        :param enable_datadog_logs: 
        :param enable_datadog_tracing: 
        :param extension_layer_version: 
        :param flush_metrics_to_logs: 
        :param forwarder_arn: 
        :param inject_log_context: 
        :param log_level: 
        :param node_layer_version: 
        :param python_layer_version: 
        :param site: 
        '''
        props = DatadogProps(
            add_layers=add_layers,
            api_key=api_key,
            api_key_secret_arn=api_key_secret_arn,
            api_kms_key=api_kms_key,
            capture_lambda_payload=capture_lambda_payload,
            enable_datadog_logs=enable_datadog_logs,
            enable_datadog_tracing=enable_datadog_tracing,
            extension_layer_version=extension_layer_version,
            flush_metrics_to_logs=flush_metrics_to_logs,
            forwarder_arn=forwarder_arn,
            inject_log_context=inject_log_context,
            log_level=log_level,
            node_layer_version=node_layer_version,
            python_layer_version=python_layer_version,
            site=site,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addForwarderToNonLambdaLogGroups")
    def add_forwarder_to_non_lambda_log_groups(
        self,
        log_groups: typing.Sequence[aws_cdk.aws_logs.ILogGroup],
    ) -> None:
        '''
        :param log_groups: -
        '''
        return typing.cast(None, jsii.invoke(self, "addForwarderToNonLambdaLogGroups", [log_groups]))

    @jsii.member(jsii_name="addLambdaFunctions")
    def add_lambda_functions(
        self,
        lambda_functions: typing.Sequence[typing.Union[aws_cdk.aws_lambda.Function, aws_cdk.aws_lambda_nodejs.NodejsFunction, aws_cdk.aws_lambda_python_alpha.PythonFunction]],
    ) -> None:
        '''
        :param lambda_functions: -
        '''
        return typing.cast(None, jsii.invoke(self, "addLambdaFunctions", [lambda_functions]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="props")
    def props(self) -> "DatadogProps":
        return typing.cast("DatadogProps", jsii.get(self, "props"))

    @props.setter
    def props(self, value: "DatadogProps") -> None:
        jsii.set(self, "props", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scope")
    def scope(self) -> constructs.Construct:
        return typing.cast(constructs.Construct, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: constructs.Construct) -> None:
        jsii.set(self, "scope", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="transport")
    def transport(self) -> "Transport":
        return typing.cast("Transport", jsii.get(self, "transport"))

    @transport.setter
    def transport(self, value: "Transport") -> None:
        jsii.set(self, "transport", value)


@jsii.data_type(
    jsii_type="datadog-cdk-constructs-v2.DatadogProps",
    jsii_struct_bases=[],
    name_mapping={
        "add_layers": "addLayers",
        "api_key": "apiKey",
        "api_key_secret_arn": "apiKeySecretArn",
        "api_kms_key": "apiKmsKey",
        "capture_lambda_payload": "captureLambdaPayload",
        "enable_datadog_logs": "enableDatadogLogs",
        "enable_datadog_tracing": "enableDatadogTracing",
        "extension_layer_version": "extensionLayerVersion",
        "flush_metrics_to_logs": "flushMetricsToLogs",
        "forwarder_arn": "forwarderArn",
        "inject_log_context": "injectLogContext",
        "log_level": "logLevel",
        "node_layer_version": "nodeLayerVersion",
        "python_layer_version": "pythonLayerVersion",
        "site": "site",
    },
)
class DatadogProps:
    def __init__(
        self,
        *,
        add_layers: typing.Optional[builtins.bool] = None,
        api_key: typing.Optional[builtins.str] = None,
        api_key_secret_arn: typing.Optional[builtins.str] = None,
        api_kms_key: typing.Optional[builtins.str] = None,
        capture_lambda_payload: typing.Optional[builtins.bool] = None,
        enable_datadog_logs: typing.Optional[builtins.bool] = None,
        enable_datadog_tracing: typing.Optional[builtins.bool] = None,
        extension_layer_version: typing.Optional[jsii.Number] = None,
        flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
        forwarder_arn: typing.Optional[builtins.str] = None,
        inject_log_context: typing.Optional[builtins.bool] = None,
        log_level: typing.Optional[builtins.str] = None,
        node_layer_version: typing.Optional[jsii.Number] = None,
        python_layer_version: typing.Optional[jsii.Number] = None,
        site: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param add_layers: 
        :param api_key: 
        :param api_key_secret_arn: 
        :param api_kms_key: 
        :param capture_lambda_payload: 
        :param enable_datadog_logs: 
        :param enable_datadog_tracing: 
        :param extension_layer_version: 
        :param flush_metrics_to_logs: 
        :param forwarder_arn: 
        :param inject_log_context: 
        :param log_level: 
        :param node_layer_version: 
        :param python_layer_version: 
        :param site: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if add_layers is not None:
            self._values["add_layers"] = add_layers
        if api_key is not None:
            self._values["api_key"] = api_key
        if api_key_secret_arn is not None:
            self._values["api_key_secret_arn"] = api_key_secret_arn
        if api_kms_key is not None:
            self._values["api_kms_key"] = api_kms_key
        if capture_lambda_payload is not None:
            self._values["capture_lambda_payload"] = capture_lambda_payload
        if enable_datadog_logs is not None:
            self._values["enable_datadog_logs"] = enable_datadog_logs
        if enable_datadog_tracing is not None:
            self._values["enable_datadog_tracing"] = enable_datadog_tracing
        if extension_layer_version is not None:
            self._values["extension_layer_version"] = extension_layer_version
        if flush_metrics_to_logs is not None:
            self._values["flush_metrics_to_logs"] = flush_metrics_to_logs
        if forwarder_arn is not None:
            self._values["forwarder_arn"] = forwarder_arn
        if inject_log_context is not None:
            self._values["inject_log_context"] = inject_log_context
        if log_level is not None:
            self._values["log_level"] = log_level
        if node_layer_version is not None:
            self._values["node_layer_version"] = node_layer_version
        if python_layer_version is not None:
            self._values["python_layer_version"] = python_layer_version
        if site is not None:
            self._values["site"] = site

    @builtins.property
    def add_layers(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("add_layers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_key_secret_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_key_secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_kms_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capture_lambda_payload(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("capture_lambda_payload")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_datadog_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_datadog_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_datadog_tracing(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_datadog_tracing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extension_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("extension_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def flush_metrics_to_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("flush_metrics_to_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def forwarder_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("forwarder_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inject_log_context(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("inject_log_context")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("node_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def python_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("python_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def site(self) -> typing.Optional[builtins.str]:
        result = self._values.get("site")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="datadog-cdk-constructs-v2.DatadogStrictProps",
    jsii_struct_bases=[],
    name_mapping={
        "add_layers": "addLayers",
        "capture_lambda_payload": "captureLambdaPayload",
        "enable_datadog_logs": "enableDatadogLogs",
        "enable_datadog_tracing": "enableDatadogTracing",
        "inject_log_context": "injectLogContext",
        "api_key": "apiKey",
        "api_key_secret_arn": "apiKeySecretArn",
        "api_kms_key": "apiKmsKey",
        "extension_layer_version": "extensionLayerVersion",
        "flush_metrics_to_logs": "flushMetricsToLogs",
        "forwarder_arn": "forwarderArn",
        "log_level": "logLevel",
        "node_layer_version": "nodeLayerVersion",
        "python_layer_version": "pythonLayerVersion",
        "site": "site",
    },
)
class DatadogStrictProps:
    def __init__(
        self,
        *,
        add_layers: builtins.bool,
        capture_lambda_payload: builtins.bool,
        enable_datadog_logs: builtins.bool,
        enable_datadog_tracing: builtins.bool,
        inject_log_context: builtins.bool,
        api_key: typing.Optional[builtins.str] = None,
        api_key_secret_arn: typing.Optional[builtins.str] = None,
        api_kms_key: typing.Optional[builtins.str] = None,
        extension_layer_version: typing.Optional[jsii.Number] = None,
        flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
        forwarder_arn: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        node_layer_version: typing.Optional[jsii.Number] = None,
        python_layer_version: typing.Optional[jsii.Number] = None,
        site: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param add_layers: 
        :param capture_lambda_payload: 
        :param enable_datadog_logs: 
        :param enable_datadog_tracing: 
        :param inject_log_context: 
        :param api_key: 
        :param api_key_secret_arn: 
        :param api_kms_key: 
        :param extension_layer_version: 
        :param flush_metrics_to_logs: 
        :param forwarder_arn: 
        :param log_level: 
        :param node_layer_version: 
        :param python_layer_version: 
        :param site: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "add_layers": add_layers,
            "capture_lambda_payload": capture_lambda_payload,
            "enable_datadog_logs": enable_datadog_logs,
            "enable_datadog_tracing": enable_datadog_tracing,
            "inject_log_context": inject_log_context,
        }
        if api_key is not None:
            self._values["api_key"] = api_key
        if api_key_secret_arn is not None:
            self._values["api_key_secret_arn"] = api_key_secret_arn
        if api_kms_key is not None:
            self._values["api_kms_key"] = api_kms_key
        if extension_layer_version is not None:
            self._values["extension_layer_version"] = extension_layer_version
        if flush_metrics_to_logs is not None:
            self._values["flush_metrics_to_logs"] = flush_metrics_to_logs
        if forwarder_arn is not None:
            self._values["forwarder_arn"] = forwarder_arn
        if log_level is not None:
            self._values["log_level"] = log_level
        if node_layer_version is not None:
            self._values["node_layer_version"] = node_layer_version
        if python_layer_version is not None:
            self._values["python_layer_version"] = python_layer_version
        if site is not None:
            self._values["site"] = site

    @builtins.property
    def add_layers(self) -> builtins.bool:
        result = self._values.get("add_layers")
        assert result is not None, "Required property 'add_layers' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def capture_lambda_payload(self) -> builtins.bool:
        result = self._values.get("capture_lambda_payload")
        assert result is not None, "Required property 'capture_lambda_payload' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_datadog_logs(self) -> builtins.bool:
        result = self._values.get("enable_datadog_logs")
        assert result is not None, "Required property 'enable_datadog_logs' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_datadog_tracing(self) -> builtins.bool:
        result = self._values.get("enable_datadog_tracing")
        assert result is not None, "Required property 'enable_datadog_tracing' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def inject_log_context(self) -> builtins.bool:
        result = self._values.get("inject_log_context")
        assert result is not None, "Required property 'inject_log_context' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_key_secret_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_key_secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_kms_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extension_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("extension_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def flush_metrics_to_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("flush_metrics_to_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def forwarder_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("forwarder_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("node_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def python_layer_version(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("python_layer_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def site(self) -> typing.Optional[builtins.str]:
        result = self._values.get("site")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogStrictProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="datadog-cdk-constructs-v2.ILambdaFunction")
class ILambdaFunction(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def node(self) -> "Node":
        ...

    @node.setter
    def node(self, value: "Node") -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> "Runtime":
        ...

    @runtime.setter
    def runtime(self, value: "Runtime") -> None:
        ...

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(
        self,
        ey: builtins.str,
        value: builtins.str,
        options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param ey: -
        :param value: -
        :param options: -
        '''
        ...


class _ILambdaFunctionProxy:
    __jsii_type__: typing.ClassVar[str] = "datadog-cdk-constructs-v2.ILambdaFunction"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def node(self) -> "Node":
        return typing.cast("Node", jsii.get(self, "node"))

    @node.setter
    def node(self, value: "Node") -> None:
        jsii.set(self, "node", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> "Runtime":
        return typing.cast("Runtime", jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: "Runtime") -> None:
        jsii.set(self, "runtime", value)

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(
        self,
        ey: builtins.str,
        value: builtins.str,
        options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param ey: -
        :param value: -
        :param options: -
        '''
        return typing.cast(None, jsii.invoke(self, "addEnvironment", [ey, value, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILambdaFunction).__jsii_proxy_class__ = lambda : _ILambdaFunctionProxy


@jsii.data_type(
    jsii_type="datadog-cdk-constructs-v2.Node",
    jsii_struct_bases=[],
    name_mapping={"default_child": "defaultChild"},
)
class Node:
    def __init__(self, *, default_child: typing.Any) -> None:
        '''
        :param default_child: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "default_child": default_child,
        }

    @builtins.property
    def default_child(self) -> typing.Any:
        result = self._values.get("default_child")
        assert result is not None, "Required property 'default_child' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Node(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="datadog-cdk-constructs-v2.Runtime",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class Runtime:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Runtime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="datadog-cdk-constructs-v2.RuntimeType")
class RuntimeType(enum.Enum):
    NODE = "NODE"
    PYTHON = "PYTHON"
    UNSUPPORTED = "UNSUPPORTED"


@jsii.enum(jsii_type="datadog-cdk-constructs-v2.TagKeys")
class TagKeys(enum.Enum):
    CDK = "CDK"


class Transport(
    metaclass=jsii.JSIIMeta,
    jsii_type="datadog-cdk-constructs-v2.Transport",
):
    def __init__(
        self,
        flush_metrics_to_logs: typing.Optional[builtins.bool] = None,
        site: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
        api_key_secret_arn: typing.Optional[builtins.str] = None,
        api_kms_key: typing.Optional[builtins.str] = None,
        extension_layer_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param flush_metrics_to_logs: -
        :param site: -
        :param api_key: -
        :param api_key_secret_arn: -
        :param api_kms_key: -
        :param extension_layer_version: -
        '''
        jsii.create(self.__class__, self, [flush_metrics_to_logs, site, api_key, api_key_secret_arn, api_kms_key, extension_layer_version])

    @jsii.member(jsii_name="applyEnvVars")
    def apply_env_vars(self, lambdas: typing.Sequence[ILambdaFunction]) -> None:
        '''
        :param lambdas: -
        '''
        return typing.cast(None, jsii.invoke(self, "applyEnvVars", [lambdas]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="flushMetricsToLogs")
    def flush_metrics_to_logs(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "flushMetricsToLogs"))

    @flush_metrics_to_logs.setter
    def flush_metrics_to_logs(self, value: builtins.bool) -> None:
        jsii.set(self, "flushMetricsToLogs", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="site")
    def site(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "site"))

    @site.setter
    def site(self, value: builtins.str) -> None:
        jsii.set(self, "site", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "apiKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiKeySecretArn")
    def api_key_secret_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeySecretArn"))

    @api_key_secret_arn.setter
    def api_key_secret_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "apiKeySecretArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiKmsKey")
    def api_kms_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKmsKey"))

    @api_kms_key.setter
    def api_kms_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "apiKmsKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="extensionLayerVersion")
    def extension_layer_version(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "extensionLayerVersion"))

    @extension_layer_version.setter
    def extension_layer_version(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "extensionLayerVersion", value)


__all__ = [
    "Datadog",
    "DatadogProps",
    "DatadogStrictProps",
    "ILambdaFunction",
    "Node",
    "Runtime",
    "RuntimeType",
    "TagKeys",
    "Transport",
]

publication.publish()

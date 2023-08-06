'''
# cdk8s-aws-lb-controller

![Release](https://github.com/opencdk8s/cdk8s-aws-lb-controller/workflows/Release/badge.svg?branch=development)
[![npm version](https://badge.fury.io/js/%40opencdk8s%2Fcdk8s-aws-lb-controller.svg)](https://badge.fury.io/js/%40opencdk8s%2Fcdk8s-aws-lb-controller)
[![PyPI version](https://badge.fury.io/py/cdk8s-aws-lb-controller.svg)](https://badge.fury.io/py/cdk8s-aws-lb-controller)
![npm](https://img.shields.io/npm/dt/@opencdk8s/cdk8s-aws-lb-controller?label=npm&color=green)
![PyPi](https://img.shields.io/pypi/dm/cdk8s-aws-lb-controller?label=pypi&color=green)

Synths an install manifest for [aws-load-balancer-controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller), based off of [this repo](https://github.com/guan840912/cdk8s-aws-load-balancer-controller)

## Controller version : `v2.2.0`

## Overview

### `install.yaml` example

```python
import { Construct } from 'constructs';
import { App, Chart, ChartProps } from 'cdk8s';
import { AwsLoadBalancerController } from '@opencdk8s/cdk8s-aws-lb-controller'

export class MyChart extends Chart {
  constructor(scope: Construct, id: string, props: ChartProps = { }) {
    super(scope, id, props);

    new AwsLoadBalancerController(this, 'example', {
      clusterName: 'example',
    })

  }
}

const app = new App();
new MyChart(app, 'example');
app.synth();
```

<details>
<summary>install.k8s.yaml</summary>

```yaml
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  annotations:
    controller-gen.kubebuilder.io/version: v0.4.0
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: targetgroupbindings.elbv2.k8s.aws
spec:
  additionalPrinterColumns:
    - JSONPath: .spec.serviceRef.name
      description: The Kubernetes Service's name
      name: SERVICE-NAME
      type: string
    - JSONPath: .spec.serviceRef.port
      description: The Kubernetes Service's port
      name: SERVICE-PORT
      type: string
    - JSONPath: .spec.targetType
      description: The AWS TargetGroup's TargetType
      name: TARGET-TYPE
      type: string
    - JSONPath: .spec.targetGroupARN
      description: The AWS TargetGroup's Amazon Resource Name
      name: ARN
      priority: 1
      type: string
    - JSONPath: .metadata.creationTimestamp
      name: AGE
      type: date
  group: elbv2.k8s.aws
  names:
    categories:
      - all
    kind: TargetGroupBinding
    listKind: TargetGroupBindingList
    plural: targetgroupbindings
    singular: targetgroupbinding
  scope: Namespaced
  subresources:
    status: {}
  validation:
    openAPIV3Schema:
      description: TargetGroupBinding is the Schema for the TargetGroupBinding API
      properties:
        apiVersion:
          description: "APIVersion defines the versioned schema of this representation of
            an object. Servers should convert recognized schemas to the latest
            internal value, and may reject unrecognized values. More info:
            https://git.k8s.io/community/contributors/devel/sig-architecture/ap\
            i-conventions.md#resources"
          type: string
        kind:
          description: "Kind is a string value representing the REST resource this object
            represents. Servers may infer this from the endpoint the client
            submits requests to. Cannot be updated. In CamelCase. More info:
            https://git.k8s.io/community/contributors/devel/sig-architecture/ap\
            i-conventions.md#types-kinds"
          type: string
        metadata:
          type: object
        spec:
          description: TargetGroupBindingSpec defines the desired state of
            TargetGroupBinding
          properties:
            networking:
              description: networking provides the networking setup for ELBV2 LoadBalancer to
                access targets in TargetGroup.
              properties:
                ingress:
                  description: List of ingress rules to allow ELBV2 LoadBalancer to access targets
                    in TargetGroup.
                  items:
                    properties:
                      from:
                        description: List of peers which should be able to access the targets in
                          TargetGroup. At least one NetworkingPeer should be
                          specified.
                        items:
                          description: NetworkingPeer defines the source/destination peer for networking
                            rules.
                          properties:
                            ipBlock:
                              description: IPBlock defines an IPBlock peer. If specified, none of the other
                                fields can be set.
                              properties:
                                cidr:
                                  description: CIDR i the network CIDR. Both IPV4 or IPV6 CIDR are accepted.
                                  type: string
                              required:
                                - cidr
                              type: object
                            securityGroup:
                              description: SecurityGroup defines a SecurityGroup peer. If specified, none of
                                the other fields can be set.
                              properties:
                                groupID:
                                  description: GroupID is the EC2 SecurityGroupID.
                                  type: string
                              required:
                                - groupID
                              type: object
                          type: object
                        type: array
                      ports:
                        description: List of ports which should be made accessible on the targets in
                          TargetGroup. If ports is empty or unspecified, it
                          defaults to all ports with TCP.
                        items:
                          properties:
                            port:
                              anyOf:
                                - type: integer
                                - type: string
                              description: The port which traffic must match. When NodePort endpoints(instance
                                TargetType) is used, this must be a numerical
                                port. When Port endpoints(ip TargetType) is
                                used, this can be either numerical or named port
                                on pods. if port is unspecified, it defaults to
                                all ports.
                              x-kubernetes-int-or-string: true
                            protocol:
                              description: The protocol which traffic must match. If protocol is unspecified,
                                it defaults to TCP.
                              enum:
                                - TCP
                                - UDP
                              type: string
                          type: object
                        type: array
                    required:
                      - from
                      - ports
                    type: object
                  type: array
              type: object
            serviceRef:
              description: serviceRef is a reference to a Kubernetes Service and ServicePort.
              properties:
                name:
                  description: Name is the name of the Service.
                  type: string
                port:
                  anyOf:
                    - type: integer
                    - type: string
                  description: Port is the port of the ServicePort.
                  x-kubernetes-int-or-string: true
              required:
                - name
                - port
              type: object
            targetGroupARN:
              description: targetGroupARN is the Amazon Resource Name (ARN) for the
                TargetGroup.
              type: string
            targetType:
              description: targetType is the TargetType of TargetGroup. If unspecified, it
                will be automatically inferred.
              enum:
                - instance
                - ip
              type: string
          required:
            - serviceRef
            - targetGroupARN
          type: object
        status:
          description: TargetGroupBindingStatus defines the observed state of
            TargetGroupBinding
          properties:
            observedGeneration:
              description: The generation observed by the TargetGroupBinding controller.
              format: int64
              type: integer
          type: object
      type: object
  version: v1alpha1
  versions:
    - name: v1alpha1
      served: true
      storage: false
    - name: v1beta1
      served: true
      storage: true
status:
  acceptedNames:
    kind: ""
    plural: ""
  conditions: []
  storedVersions: []
---
apiVersion: admissionregistration.k8s.io/v1beta1
kind: MutatingWebhookConfiguration
metadata:
  annotations:
    cert-manager.io/inject-ca-from: kube-system/aws-load-balancer-serving-cert
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-webhook
webhooks:
  - clientConfig:
      caBundle: Cg==
      service:
        name: aws-load-balancer-webhook-service
        namespace: kube-system
        path: /mutate-v1-pod
    failurePolicy: Fail
    name: mpod.elbv2.k8s.aws
    namespaceSelector:
      matchExpressions:
        - key: elbv2.k8s.aws/pod-readiness-gate-inject
          operator: In
          values:
            - enabled
    rules:
      - apiGroups:
          - ""
        apiVersions:
          - v1
        operations:
          - CREATE
        resources:
          - pods
    sideEffects: None
  - clientConfig:
      caBundle: Cg==
      service:
        name: aws-load-balancer-webhook-service
        namespace: kube-system
        path: /mutate-elbv2-k8s-aws-v1beta1-targetgroupbinding
    failurePolicy: Fail
    name: mtargetgroupbinding.elbv2.k8s.aws
    rules:
      - apiGroups:
          - elbv2.k8s.aws
        apiVersions:
          - v1beta1
        operations:
          - CREATE
          - UPDATE
        resources:
          - targetgroupbindings
    sideEffects: None
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-controller
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-controller-leader-election-role
  namespace: kube-system
rules:
  - apiGroups:
      - ""
    resources:
      - configmaps
    verbs:
      - create
  - apiGroups:
      - ""
    resourceNames:
      - aws-load-balancer-controller-leader
    resources:
      - configmaps
    verbs:
      - get
      - update
      - patch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-controller-role
rules:
  - apiGroups:
      - ""
    resources:
      - endpoints
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - events
    verbs:
      - create
      - patch
  - apiGroups:
      - ""
    resources:
      - namespaces
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - nodes
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - pods
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - pods/status
    verbs:
      - patch
      - update
  - apiGroups:
      - ""
    resources:
      - secrets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - services
    verbs:
      - get
      - list
      - patch
      - update
      - watch
  - apiGroups:
      - ""
    resources:
      - services/status
    verbs:
      - patch
      - update
  - apiGroups:
      - elbv2.k8s.aws
    resources:
      - targetgroupbindings
    verbs:
      - create
      - delete
      - get
      - list
      - patch
      - update
      - watch
  - apiGroups:
      - elbv2.k8s.aws
    resources:
      - targetgroupbindings/status
    verbs:
      - patch
      - update
  - apiGroups:
      - extensions
    resources:
      - ingresses
    verbs:
      - get
      - list
      - patch
      - update
      - watch
  - apiGroups:
      - extensions
    resources:
      - ingresses/status
    verbs:
      - patch
      - update
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses
    verbs:
      - get
      - list
      - patch
      - update
      - watch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingressclasses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses/status
    verbs:
      - patch
      - update
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-controller-leader-election-rolebinding
  namespace: kube-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: aws-load-balancer-controller-leader-election-role
subjects:
  - kind: ServiceAccount
    name: aws-load-balancer-controller
    namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-controller-rolebinding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: aws-load-balancer-controller-role
subjects:
  - kind: ServiceAccount
    name: aws-load-balancer-controller
    namespace: kube-system
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-webhook-service
  namespace: kube-system
spec:
  ports:
    - port: 443
      targetPort: 9443
  selector:
    app.kubernetes.io/component: controller
    app.kubernetes.io/name: aws-load-balancer-controller
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-controller
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/component: controller
      app.kubernetes.io/name: aws-load-balancer-controller
  template:
    metadata:
      labels:
        app.kubernetes.io/component: controller
        app.kubernetes.io/name: aws-load-balancer-controller
    spec:
      containers:
        - args:
            - --ingress-class=alb
            - --cluster-name=example
          image: amazon/aws-alb-ingress-controller:v2.1.3
          livenessProbe:
            failureThreshold: 2
            httpGet:
              path: /healthz
              port: 61779
              scheme: HTTP
            initialDelaySeconds: 30
            timeoutSeconds: 10
          name: controller
          ports:
            - containerPort: 9443
              name: webhook-server
              protocol: TCP
          resources:
            limits:
              cpu: 200m
              memory: 500Mi
            requests:
              cpu: 100m
              memory: 200Mi
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
          volumeMounts:
            - mountPath: /tmp/k8s-webhook-server/serving-certs
              name: cert
              readOnly: true
      securityContext:
        fsGroup: 1337
      serviceAccountName: aws-load-balancer-controller
      terminationGracePeriodSeconds: 10
      volumes:
        - name: cert
          secret:
            defaultMode: 420
            secretName: aws-load-balancer-webhook-tls
---
apiVersion: cert-manager.io/v1alpha2
kind: Certificate
metadata:
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-serving-cert
  namespace: kube-system
spec:
  dnsNames:
    - aws-load-balancer-webhook-service.kube-system.svc
    - aws-load-balancer-webhook-service.kube-system.svc.cluster.local
  issuerRef:
    kind: Issuer
    name: aws-load-balancer-selfsigned-issuer
  secretName: aws-load-balancer-webhook-tls
---
apiVersion: cert-manager.io/v1alpha2
kind: Issuer
metadata:
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-selfsigned-issuer
  namespace: kube-system
spec:
  selfSigned: {}
---
apiVersion: admissionregistration.k8s.io/v1beta1
kind: ValidatingWebhookConfiguration
metadata:
  annotations:
    cert-manager.io/inject-ca-from: kube-system/aws-load-balancer-serving-cert
  labels:
    app.kubernetes.io/name: aws-load-balancer-controller
  name: aws-load-balancer-webhook
webhooks:
  - clientConfig:
      caBundle: Cg==
      service:
        name: aws-load-balancer-webhook-service
        namespace: kube-system
        path: /validate-elbv2-k8s-aws-v1beta1-targetgroupbinding
    failurePolicy: Fail
    name: vtargetgroupbinding.elbv2.k8s.aws
    rules:
      - apiGroups:
          - elbv2.k8s.aws
        apiVersions:
          - v1beta1
        operations:
          - CREATE
          - UPDATE
        resources:
          - targetgroupbindings
    sideEffects: None
```

</details>

## Installation

### TypeScript

Use `yarn` or `npm` to install.

```sh
$ npm install @opencdk8s/cdk8s-aws-lb-controller
```

```sh
$ yarn add @opencdk8s/cdk8s-aws-lb-controller
```

### Python

```sh
$ pip install cdk8s-aws-lb-controller
```

## Contribution

1. Fork ([link](https://github.com/opencdk8s/cdk8s-aws-lb-controller/fork))
2. Bootstrap the repo:

   ```bash
   npx projen   # generates package.json
   yarn install # installs dependencies
   ```
3. Development scripts:
   |Command|Description
   |-|-
   |`yarn compile`|Compiles typescript => javascript
   |`yarn watch`|Watch & compile
   |`yarn test`|Run unit test & linter through jest
   |`yarn test -u`|Update jest snapshots
   |`yarn run package`|Creates a `dist` with packages for all languages.
   |`yarn build`|Compile + test + package
   |`yarn bump`|Bump version (with changelog) based on [conventional commits]
   |`yarn release`|Bump + push to `master`
4. Create a feature branch
5. Commit your changes
6. Rebase your local changes against the master branch
7. Create a new Pull Request (use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for the title please)

## Licence

[Apache License, Version 2.0](./LICENSE)

## Author

[Hunter-Thompson](https://github.com/Hunter-Thompson)
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

import constructs


class AwsLoadBalancerController(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@opencdk8s/cdk8s-aws-lb-controller.AwsLoadBalancerController",
):
    '''(experimental) Generate aws-load-balancer-controller config yaml.

    see https://github.com/kubernetes-sigs/aws-aws-load-balancer-controller/blob/master/docs/install/v2_0_0_full.yaml

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_name: builtins.str,
        service_account_name: builtins.str,
        argo_cert_ignore: typing.Optional[builtins.bool] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        cert_manager: typing.Optional[builtins.bool] = None,
        create_service_account: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Sequence["EnvVar"]] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster_name: (experimental) Kubernetes Cluster Name for aws-load-balancer-controller. Default: - None
        :param service_account_name: (experimental) Service Account Name for aws-load-balancer-controller. Default: - aws-load-balancer-controller
        :param argo_cert_ignore: (experimental) Add an annotation so that ArgoCD ignores mutatingwebhook.
        :param args: (experimental) Another Args for aws-load-balancer-controller. Default: - None
        :param cert_manager: (experimental) Install cert-manager. Default: - true
        :param create_service_account: (experimental) service account for aws-load-balancer-controller. Default: - true
        :param env: (experimental) Another Args for aws-load-balancer-controller. Default: - None
        :param image: (experimental) Default image for aws-load-balancer-controller. Default: - docker.io/amazon/aws-aws-load-balancer-controller:v1.1.9
        :param labels: (experimental) Extra labels to associate with resources. Default: - none
        :param namespace: (experimental) Default Namespace for aws-load-balancer-controller. Default: - kube-system
        :param replicas: (experimental) Replicas for aws-load-balancer-controller. Default: - 1

        :stability: experimental
        '''
        options = AwsLoadBalancerControllerOptions(
            cluster_name=cluster_name,
            service_account_name=service_account_name,
            argo_cert_ignore=argo_cert_ignore,
            args=args,
            cert_manager=cert_manager,
            create_service_account=create_service_account,
            env=env,
            image=image,
            labels=labels,
            namespace=namespace,
            replicas=replicas,
        )

        jsii.create(self.__class__, self, [scope, id, options])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        '''(experimental) Kubernetes Cluster Name for aws-load-balancer-controller.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentName")
    def deployment_name(self) -> builtins.str:
        '''(experimental) Kubernetes Deployment Name for aws-load-balancer-controller.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        '''(experimental) Namespace for aws-load-balancer-controller.

        :default: - kube-system

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceAccountName")
    def service_account_name(self) -> builtins.str:
        '''(experimental) Service Account Name for aws-load-balancer-controller.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certManager")
    def cert_manager(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install cert manager.

        :default: - true

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "certManager"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="createServiceAccount")
    def create_service_account(self) -> typing.Optional[builtins.bool]:
        '''(experimental) service account for aws-load-balancer-controller.

        :default: - true

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "createServiceAccount"))


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-aws-lb-controller.AwsLoadBalancerControllerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "service_account_name": "serviceAccountName",
        "argo_cert_ignore": "argoCertIgnore",
        "args": "args",
        "cert_manager": "certManager",
        "create_service_account": "createServiceAccount",
        "env": "env",
        "image": "image",
        "labels": "labels",
        "namespace": "namespace",
        "replicas": "replicas",
    },
)
class AwsLoadBalancerControllerOptions:
    def __init__(
        self,
        *,
        cluster_name: builtins.str,
        service_account_name: builtins.str,
        argo_cert_ignore: typing.Optional[builtins.bool] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        cert_manager: typing.Optional[builtins.bool] = None,
        create_service_account: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Sequence["EnvVar"]] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cluster_name: (experimental) Kubernetes Cluster Name for aws-load-balancer-controller. Default: - None
        :param service_account_name: (experimental) Service Account Name for aws-load-balancer-controller. Default: - aws-load-balancer-controller
        :param argo_cert_ignore: (experimental) Add an annotation so that ArgoCD ignores mutatingwebhook.
        :param args: (experimental) Another Args for aws-load-balancer-controller. Default: - None
        :param cert_manager: (experimental) Install cert-manager. Default: - true
        :param create_service_account: (experimental) service account for aws-load-balancer-controller. Default: - true
        :param env: (experimental) Another Args for aws-load-balancer-controller. Default: - None
        :param image: (experimental) Default image for aws-load-balancer-controller. Default: - docker.io/amazon/aws-aws-load-balancer-controller:v1.1.9
        :param labels: (experimental) Extra labels to associate with resources. Default: - none
        :param namespace: (experimental) Default Namespace for aws-load-balancer-controller. Default: - kube-system
        :param replicas: (experimental) Replicas for aws-load-balancer-controller. Default: - 1

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_name": cluster_name,
            "service_account_name": service_account_name,
        }
        if argo_cert_ignore is not None:
            self._values["argo_cert_ignore"] = argo_cert_ignore
        if args is not None:
            self._values["args"] = args
        if cert_manager is not None:
            self._values["cert_manager"] = cert_manager
        if create_service_account is not None:
            self._values["create_service_account"] = create_service_account
        if env is not None:
            self._values["env"] = env
        if image is not None:
            self._values["image"] = image
        if labels is not None:
            self._values["labels"] = labels
        if namespace is not None:
            self._values["namespace"] = namespace
        if replicas is not None:
            self._values["replicas"] = replicas

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''(experimental) Kubernetes Cluster Name for aws-load-balancer-controller.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_account_name(self) -> builtins.str:
        '''(experimental) Service Account Name for aws-load-balancer-controller.

        :default: - aws-load-balancer-controller

        :stability: experimental
        '''
        result = self._values.get("service_account_name")
        assert result is not None, "Required property 'service_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def argo_cert_ignore(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add an annotation so that ArgoCD ignores mutatingwebhook.

        :stability: experimental
        '''
        result = self._values.get("argo_cert_ignore")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Another Args for aws-load-balancer-controller.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cert_manager(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Install cert-manager.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("cert_manager")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def create_service_account(self) -> typing.Optional[builtins.bool]:
        '''(experimental) service account for aws-load-balancer-controller.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("create_service_account")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.List["EnvVar"]]:
        '''(experimental) Another Args for aws-load-balancer-controller.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.List["EnvVar"]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Default image for aws-load-balancer-controller.

        :default: - docker.io/amazon/aws-aws-load-balancer-controller:v1.1.9

        :stability: experimental
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Extra labels to associate with resources.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) Default Namespace for aws-load-balancer-controller.

        :default: - kube-system

        :stability: experimental
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Replicas for aws-load-balancer-controller.

        :default: - 1

        :stability: experimental
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsLoadBalancerControllerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsLoadBalancerPolicy(
    metaclass=jsii.JSIIMeta,
    jsii_type="@opencdk8s/cdk8s-aws-lb-controller.AwsLoadBalancerPolicy",
):
    '''(experimental) awsLoadBalancerPolicy class ,help you add policy to your Iam Role for service account.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addPolicy") # type: ignore[misc]
    @builtins.classmethod
    def add_policy(cls, version: builtins.str, role: typing.Any) -> typing.Any:
        '''
        :param version: -
        :param role: -

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.sinvoke(cls, "addPolicy", [version, role]))


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-aws-lb-controller.EnvVar",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class EnvVar:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: (experimental) Name of the environment variable. Must be a C_IDENTIFIER.
        :param value: (experimental) Variable references $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Defaults to "". Default: .

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the environment variable.

        Must be a C_IDENTIFIER.

        :stability: experimental
        :schema: io.k8s.api.core.v1.EnvVar#name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''(experimental) Variable references $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables.

        If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Defaults to "".

        :default: .

        :stability: experimental
        :schema: io.k8s.api.core.v1.EnvVar#value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvVar(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@opencdk8s/cdk8s-aws-lb-controller.VersionsLists")
class VersionsLists(enum.Enum):
    '''
    :stability: experimental
    '''

    AWS_LOAD_BALANCER_CONTROLLER_POLICY_V2 = "AWS_LOAD_BALANCER_CONTROLLER_POLICY_V2"
    '''
    :stability: experimental
    '''


__all__ = [
    "AwsLoadBalancerController",
    "AwsLoadBalancerControllerOptions",
    "AwsLoadBalancerPolicy",
    "EnvVar",
    "VersionsLists",
]

publication.publish()

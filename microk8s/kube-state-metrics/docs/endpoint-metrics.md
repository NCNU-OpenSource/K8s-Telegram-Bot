# Endpoint Metrics

| Metric name| Metric type | Labels/tags | Status |
| ---------- | ----------- | ----------- | ----------- |
| kube_endpoint_annotations | Gauge | `endpoint`=&lt;endpoint-name&gt; <br> `namespace`=&lt;endpoint-namespace&gt; <br> `annotation_ENDPOINT_ANNOTATION`=&lt;ENDPOINT_ANNOTATION&gt;  | EXPERIMENTAL |
| kube_endpoint_address_not_ready | Gauge | `endpoint`=&lt;endpoint-name&gt; <br> `namespace`=&lt;endpoint-namespace&gt; | DEPRECATED |
| kube_endpoint_address_available | Gauge | `endpoint`=&lt;endpoint-name&gt; <br> `namespace`=&lt;endpoint-namespace&gt; | DEPRECATED |
| kube_endpoint_info | Gauge | `endpoint`=&lt;endpoint-name&gt; <br> `namespace`=&lt;endpoint-namespace&gt;  | STABLE |
| kube_endpoint_labels | Gauge | `endpoint`=&lt;endpoint-name&gt; <br> `namespace`=&lt;endpoint-namespace&gt; <br> `label_ENDPOINT_LABEL`=&lt;ENDPOINT_LABEL&gt;  | STABLE |
| kube_endpoint_created | Gauge | `endpoint`=&lt;endpoint-name&gt; <br> `namespace`=&lt;endpoint-namespace&gt; | STABLE |
| kube_endpoint_ports | Gauge | `endpoint`=&lt;endpoint-name&gt; <br> `namespace`=&lt;endpoint-namespace&gt; <br> `port_name`=&lt;endpoint-port-name&gt; <br> `port_protocol`=&lt;endpoint-port-protocol&gt; <br> `port_number`=&lt;endpoint-port-number&gt; | STABLE |
| kube_endpoint_address | Gauge | `endpoint`=&lt;endpoint-name&gt; <br> `namespace`=&lt;endpoint-namespace&gt; <br> `ip`=&lt;endpoint-ip&gt; <br> `ready`=&lt;true if available, false if unavailalbe&gt; | STABLE |

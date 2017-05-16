# fluepy - A dynamic dns updater backed by etcd

fluepy updates ddns entries using records pulled from etcd. It is designed to work in conjunction with watchtower which posts said records to etcd.

Configuration
All configuration lives in flue.json.
*	The etcd host and port can be configured using ETCD_HOST and ETCD_PORT respectively.
*	ETCD_ROOT_KEY specifies to root to look for records in etcd.
*	DNS_HOST defines the ip or hostname where the dns server to push updates to lives.
*	RNDC_KEY holds to key used for updates in the format {"key_name": "rndc_key"}
*	POLL_TIME defines the interval in seconds to poll etcd for records
*	RECORD_TTL defines to Time to Live in seconds for records pushed to the dns server. Note that this does not mean that the records expire after this time, this only defines amount of time a client will wait before requerying the dns server for the ip
*	DNS_ZONE specifies the zone in which to insert the records eg. qith this set to "example" records will be added as "host1.example" "host2.example" etc.
*	LOG_ROTATION enables log rotation, by default this will keep 2 kilobytes of logs before rotating and kepp 2 backup log files.

import enum

class TimeUnit(enum.Enum):
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


class AlertFields(enum.Enum):
    ALERT_ID = 'alert.id'
    ALERT_STATUS = 'alert.status'
    ALERT_TIME = 'alert.time'
    CLOUD_ACCOUNT_ID = 'cloud.accountId'
    CLOUD_ACCOUNT = 'cloud.account'
    CLOUD_REGION = 'cloud.region'
    RESOURCE_ID = 'resource.id'
    RESOURCE_NAME = 'resource.name'
    POLICY_NAME = 'policy.name'
    POLICY_TYPE = 'policy.type'
    POLICY_SEVERITY = 'policy.severity'


class PolicySeverity(enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class PolicyType(enum.Enum):
    CONFIG = 'config'
    NETWORK = 'network'
    AUDIT_EVENT = 'audit_event'


class AlertStatus(enum.Enum):
    OPEN = 'open'
    DISMISSED = 'dissmissed'
    SNOOZED = 'snoozed'
    RESOLVED = 'resolved'

class ScanStatus(enum.Enum):
    ALL = 'all'
    PASSED = 'passed'
    FAILED = 'failed'

class GroupBy(enum.Enum):
    CLOUD_TYPE = 'cloud.type'
    CLOUD_ACCOUNT = 'cloud.account'
    CLOUD_REGION = 'cloud.region'
    CLOUD_SERVICE = 'cloud.service'
    RESOURCE_TYPE = 'resource.type'

class CloudType(enum.Enum):
    AZURE = 'Azure'
    AWS = 'AWS'
    GCP = 'GCP'
    OCI = 'OCI'
    ALIBABA = 'Alibaba Cloud'
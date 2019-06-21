import oss2

auth = oss2.Auth('LTAI6huPFcsniRHT', 'Qo7kumR85OhK6nbez0IVKyTWYX4Beq')
bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'bucket-for-2019-hitsz')
# 内网访问，实际生产中使用
# bucket = oss2.Bucket(auth, 'oss-cn-shenzhen-internal.aliyuncs.com', 'bucket-for-2019-hitsz')

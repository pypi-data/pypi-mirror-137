import yaml
import consul
ENVIRONMENT='devel'
#Nilai ENVIRONMENT akan berubah otomatis pada waktu build di AWS-EKS
def load_config() -> dict:
    if ENVIRONMENT=='production' or ENVIRONMENT=='staging':
        #jangan ubah, proses build prod akan otomatis replace string host='consul-staging' menjadi 'consul' (prod)
        #link setting consul staging: http://10.8.0.1:8501/ui/dc1/kv/config/crm/setting/edit
        c = consul.Consul(host='consul-staging', port=8500)
        index, data = c.kv.get('config/crm/setting')
        config = yaml.load(data['Value'],Loader=yaml.SafeLoader)
        return config
    else:
        #setting config memakai file local
        with open('config/setting.yml') as yaml_file:
            conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
        return conf
import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
import requests
import json
from apitoken import API_TOKEN
from urls import *
from datetime import datetime
import re

HEADERS = { 'Authorization': API_TOKEN, }

t_date = datetime.now().strftime('%d_%m_%Y')

responsecluster = requests.get(URL_CLUSTER, headers=HEADERS)
resultcluster = responsecluster.json()
c = len (resultcluster["data"]) 


class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        for i in range (c):
            clusterN = i
            clustername=resultcluster["data"][clusterN]["spec"]["displayName"]
            clusterid=resultcluster["data"][clusterN]["id"]

            url_clusters = URL_CLUSTERS+clusterid
            responseresource = requests.get(url_clusters, headers=HEADERS)
            resultlresource = responseresource.json()

            try:
                memory = resultlresource["capacity"]["memory"]
                memory = re.sub(r'\D', "", memory) 
            except:
                memory = 0
            g = GaugeMetricFamily("capacity_cluster_memory", 'Cluster capacity Memory in Gb', labels=['cluster'])
            g.add_metric([clustername],value=int(memory)/1024/1024)
            yield g

            try:
                cpu = resultlresource["capacity"]["cpu"]
                cpu = re.sub(r'\D', "", cpu) 
            except:
                cpu = 0
            g = GaugeMetricFamily("capacity_cluster_cpu", 'Cluster capacity Cpu ', labels=['cluster'])
            g.add_metric([clustername],value=cpu)
            yield g

            try:
                pods = resultlresource["capacity"]["pods"]
                pods = re.sub(r'\D', "", pods) 
            except:
                pods = 0
            g = GaugeMetricFamily("capacity_cluster_pods", 'Cluster capacity pods ', labels=['cluster'])
            g.add_metric([clustername],value=pods)
            yield g

           
            
            url_project = URL_PROJECT+clusterid
            responseproject = requests.get(url_project, headers=HEADERS)
            resultproject = responseproject.json() 
            p = len (resultproject["data"])
            for a in range (p):      
                projectN = a
                projectname=resultproject["data"][projectN]["metadata"]["name"]
                projectName=resultproject["data"][projectN]["spec"]["displayName"]
                projectid = resultproject["data"][projectN]["id"]

#                with open(f'project_{t_date}_{projectName}_{clustername}.json', 'w') as f:
#                    f.write(json.dumps(resultproject))
                url_limits=URL_LIMITS+clusterid+":"+projectname
#                print(url_limits)
                responselimits = requests.get(url_limits, headers=HEADERS)
                resultlimits = responselimits.json()
                
                try:    
                    system_id = str(resultlimits["labels"]["system_id"])
                    #system_id = re.sub(r'\D', "", system_id)
                except:
                    system_id = "None"

                               
                try:
                    limitsCpu = resultlimits["resourceQuota"]["limit"]["limitsCpu"]
                    limitsCpu = re.sub(r'\D', "", limitsCpu) 
                except:
                    limitsCpu = 0
                print(clustername +" " + projectName + " limitsCpu = " + str(limitsCpu) +"  system_id = " + str(system_id))
                g = GaugeMetricFamily("limitsCpu_project", 'Project resourceQuota limits Cpu ', labels=['cluster','project','system_id'])
                g.add_metric([clustername,projectName,system_id],value=limitsCpu)
                yield g

                try:
                    limitsMemory = resultlimits["resourceQuota"]["limit"]["limitsMemory"]
                    limitsMemory = re.sub(r'\D', "", limitsMemory) 
                except:
                    limitsCpu = 0
#                print(clustername +" " + projectName + " limitsMemory = ",limitsMemory)
                g = GaugeMetricFamily("limitsMemory_project", 'Project resourceQuota limitsMemory ', labels=['cluster','project','system_id'])
                g.add_metric([clustername,projectName,system_id],value=limitsMemory)
                yield g

                try:
                    requestsStorage = resultlimits["resourceQuota"]["limit"]["requestsStorage"]
                    requestsStorage = re.sub(r'\D', "", requestsStorage) 
                except:
                    requestsStorage = 0
#                print(clustername +" " + projectName + " requestsStorage = ",requestsStorage)
                g = GaugeMetricFamily("requestsStorage_project", 'Project resourceQuota requestsStorage ', labels=['cluster','project','system_id'])
                g.add_metric([clustername,projectName,system_id],value=requestsStorage)
                yield g

                try:
                    requestsCpu = resultlimits["resourceQuota"]["limit"]["requestsCpu"]
                    requestsCpu = re.sub(r'\D', "", requestsCpu) 
                except:
                    limitsCpu = 0
#                print(clustername +" " + projectName + " requestsCpu = ",requestsCpu)
                g = GaugeMetricFamily("requestsCpu_project", 'Project resourceQuota requestsCpu ', labels=['cluster','project','system_id'])
                g.add_metric([clustername,projectName,system_id],value=requestsCpu)
                yield g

                try:
                    requestsMemory = resultlimits["resourceQuota"]["limit"]["requestsMemory"]
                    requestsMemory = re.sub(r'\D', "", requestsMemory) 
                except:
                    requestsMemory = 0
#                print(clustername +" " + projectName + " requestsMemory = ",requestsMemory)
                g = GaugeMetricFamily("requestsMemory_project", 'Project resourceQuota requestsMemory ', labels=['cluster','project','system_id'])
                g.add_metric([clustername,projectName,system_id],value=requestsMemory)
                yield g


                try:
                    persistentVolumeClaims = resultlimits["resourceQuota"]["limit"]["persistentVolumeClaims"]
                    persistentVolumeClaims = re.sub(r'\D', "", persistentVolumeClaims) 
                except:
                    persistentVolumeClaims = 0
#                print(clustername +" " + projectName + " requestsMemory = ",persistentVolumeClaims)
                g = GaugeMetricFamily("persistentVolumeClaims_project", 'Project resourceQuota persistentVolumeClaims ', labels=['cluster','project','system_id'])
                g.add_metric([clustername,projectName,system_id],value=persistentVolumeClaims)
                yield g


            url_namespaces = URL_NAMESPACES+clusterid+'/namespaces/'
#            print(url_namespaces)
            responsenamespaces = requests.get(url_namespaces, headers=HEADERS)
            resultnamespaces = responsenamespaces.json() 
            n = len (resultnamespaces["data"])
#            print(n)
            for e in range (n):      
                namespaceN = e
                # namespacename=resultnamespaces["data"][namespaceN]["links"]["name"]
                # namespaceName=resultnamespaces["data"][namespaceN]["links"]["displayName"]
                namespacename = resultnamespaces["data"][namespaceN]["name"]
#                print(namespacename)
                #                with open(f'project_{t_date}_{projectName}_{clustername}.json', 'w') as f:
                #                    f.write(json.dumps(resultproject))
                # url_namespace=URL_NAMESPACES+clusterid+'/namespaces/'+namespacename
                # responsenamelimits = requests.get(url_namespace, headers=HEADERS)
                # resultnamelimits = responsenamelimits.json()
                try:
                    requestsCpu = resultnamespaces["data"][namespaceN]["resourceQuota"]["limit"]["requestsCpu"]
                    requestsCpu = re.sub(r'\D', "", requestsCpu) 
                except:
                    requestsCpu = 0
#                    print(clustername +" " + projectName + " " + namespacename + " requestsCpu = ",requestsCpu)
                    g = GaugeMetricFamily("requestsCpu_namespace", 'namespace resourceQuota requestsCpu ', labels=['cluster','project','namespace','system_id'])
                    g.add_metric([clustername,projectName,namespacename,system_id],value=requestsCpu)
                yield g

                try:
                    requestsMemory = resultnamespaces["data"][namespaceN]["resourceQuota"]["limit"]["requestsMemory"]
                    requestsMemory = re.sub(r'\D', "", requestsMemory) 
                except:
                    requestsMemory = 0
#                    print(clustername +" " + projectName + " " + namespacename + " requestsMemory = ",requestsMemory)
                    g = GaugeMetricFamily("requestsMemory_namespace", 'namespace resourceQuota requestsMemory ', labels=['cluster','project','namespace','system_id'])
                    g.add_metric([clustername,projectName,namespacename,system_id],value=requestsMemory)
                yield g

                try:
                    requestsStorage = resultnamespaces["data"][namespaceN]["resourceQuota"]["limit"]["requestsStorage"]
                    requestsStorage = re.sub(r'\D', "", requestsStorage) 
                except:
                    requestsStorage = 0
#                    print(clustername +" " + projectName + " " + namespacename + " requestsStorage = ",requestsStorage)
                    g = GaugeMetricFamily("requestsStorage_namespace", 'namespace resourceQuota requestsStorage ', labels=['cluster','project','namespace','system_id'])
                    g.add_metric([clustername,projectName,namespacename,system_id],value=requestsStorage)
                yield g


if __name__ == '__main__':
    start_http_server(8003)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)

from UserAgentwithProxys import UserAgentwithProxy
import random
import base64

class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(UserAgentwithProxy.user_agent_list)
        #print useragent
        request.headers.setdefault("User-Agent", useragent)

class RandomProxy(object):
    def process_request(self, request, spider):
        proxy=random.choice(UserAgentwithProxy.proxy_list)
        #print proxy
        #if proxy['user_passwd'] is None:
        '''try:
            request.meta['proxy'] = "http://" + proxy['ip_port']
        except:
            proxy=random.choice(UserAgentwithProxy.proxy_list)
            request.meta['proxy'] = "http://" + proxy['ip_port']
        else:
            base64_userpasswd = base64.b64encode(proxy['user_passwd'])
            request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd
            request.meta['proxy'] = "http://" + proxy['ip_port']'''



class SessionConfig:
    api_uri: str = 'http://localhost:4000'
    api_key: str = ''
    botname: str = ''
    

def configure_client(api_uri='http://localhost:4000', api_key='', botname=''):
    SessionConfig.api_uri = api_uri
    SessionConfig.api_key = api_key
    SessionConfig.botname = botname


if __name__ == '__main__':
    
    configure_client('http://test.com', b'test')
    config = SessionConfig()
    config2 = SessionConfig()
    config2.api_uri = 'http://test2.com'
    print(config.api_uri, config.api_key)
    print(config2.api_uri)


    class TestConf(SessionConfig):
        pass
    config3 = TestConf()
    print(config3.api_uri)
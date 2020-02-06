from guy import Guy,http

@http(r"/item/(\d+)") 
def getItem(web,number):
  web.write( "item %s"%number )


def test_hook_with_classic_fetch(runner):
    class T(Guy):
        __doc__="""Hello
        <script>
        async function testHook() {
            var r=await window.fetch("/item/42")
            return await r.text()
        }
        </script>
        """
        async def init(self):
            self.retour =await self.js.testHook()
            self.exit()

    t=T()
    r=runner(t)
    assert r.retour == "item 42"


def test_hook_with_classic_fetch(runner): # same concept as test_600_redirect.py ... but with better url
    db={}

    class Simplest(Guy):
        """
        <script>
        function init() {
            self.end( "<<msg>>" )
        }
        </script>
        """
        def __init__(self,txt):
            Guy.__init__(self)
            self.msg=txt

        async def init(self):
            await self.js.init()

        def end(self,txt):
            db["retour"] = txt
            self.exit()

    @http(r"/myhookrunwindow/(.+)")
    def myhook(web,msg):
        return Simplest(msg)

    class T(Guy):
        """Hello
        <script>
        function start() {
            document.location.href="/myhookrunwindow/Hook Window";
        }
        </script>
        """
        async def init(self):
            await self.js.start()

    t=T()
    runner(t) # the returned instance is the main (t)
    assert db["retour"] == "Hook Window"

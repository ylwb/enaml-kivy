#------------------------------------------------------------------------------
# Copyright (c) 2016, frmdstryr.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
import enaml
from enamlkv.kv.kv_application import KvApplication

class EnamlKvApp(KvApplication):
    def build(self):
        with enaml.imports():
            from hello_world_view import Main
            
        view = Main(message="Hello World, from Python!")
        view.show()
        
        return super(EnamlKvApp, self).build()

def main():
    app = EnamlKvApp()
    app.start()


if __name__ == "__main__":
    main()

#! /usr/bin/env python

import config
from views import views

conf = config.get_config()
log = config.configure_logging()
app = config.get_app()
bind_ip = conf.get('server', 'bind_ip')
bind_port = conf.getint('server', 'bind_port')
debug_mode = conf.get('general', 'debug_mode')
log.debug('Binding to ' + bind_ip + ':' + str(bind_port))

app.register_blueprint(views)


if __name__ == "__main__":
   app.run(debug=debug_mode, host=bind_ip, port=bind_port)

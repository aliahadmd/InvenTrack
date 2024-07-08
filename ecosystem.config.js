// edit based on your project path
module.exports = {
    apps: [{
      name: "Inventrack",
      script: "/home/p/production/InvenTrack/.venv/bin/gunicorn",
      args: "--config gunicorn_config.py core.wsgi:application",
      cwd: "/home/p/production/InvenTrack",
      interpreter: "/home/p/production/InvenTrack/.venv/bin/python",
    }]
  }
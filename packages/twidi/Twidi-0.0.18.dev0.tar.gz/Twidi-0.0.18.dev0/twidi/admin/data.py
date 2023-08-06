import json
import os.path

from sqlalchemy import update

from twidi.admin import db
from twidi.admin.models import Cog, Device, Command, CommandTrigger, NoteMessage, ControlMessage, Configuration, \
    PointRedemption
from twidi.device import device_manager


def load_redemptions_from_json(json_data=None):
    if not json_data:
        current_dir = os.path.abspath(__file__)
        data_file = os.path.dirname(current_dir)
        p = os.path.join(data_file, 'data/redemptions.json')
        with open(p) as f:
            redemptions = json.load(f)
    else:
        redemptions = json_data

    for r in redemptions.get('data'):
        id = r.get('id')
        redemption = db.session.query(PointRedemption).filter(PointRedemption.id == id).first()

        cooldown = r.get('global_cooldown_setting', {'global_cooldown_seconds': 0})
        args = {
            'id': r.get('id', None),
            'title': r.get('title', 'No Title'),
            'cost': r.get('cost', 0),
            'enabled': r.get('enabled', False),
            'prompt': r.get('prompt', ''),
            'cooldown_in_seconds': cooldown.get('global_cooldown_seconds', 0)
        }

        if redemption:
            id = args.pop('id')
            db.session.execute(
                update(PointRedemption).
                    where(PointRedemption.id == id)
                    .values(**args))
        else:
            p = PointRedemption(**args)
            db.session.add(p)
            print('Added redemption: {}'.format(args.get('title')))


def create_database(recreate=True):
    if recreate:
        db.drop_all()
        db.create_all()

    def update_devices():
        ids = device_manager.get_device_ids()
        inputs = ids.get('outputs')
        device = None
        for i in inputs:
            existing_device = db.session.query(Device).filter(Device.device_id == i).first()
            if not existing_device:
                d = Device(label=i, device_id=i)
                if not device:
                    device = d
                db.session.add(
                    d
                )


    def create_credentials():
        config = dict(
            {
                "broadcaster_id": '79572160',
                "broadcaster_access_token": 'Replace',
                "broadcaster_client_token": 'Replace',
                "broadcaster_refresh_token": '',
                "bot_access_token": 'Replace',
                "bot_client_token": ''
            }
        )

        c: Configuration = Configuration(**config)
        db.session.add(c)

    update_devices()
    if recreate:
        load_redemptions_from_json()
        create_credentials()
    db.session.commit()

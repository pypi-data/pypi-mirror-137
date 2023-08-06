from twitchio.ext import pubsub
from twitchio.ext.commands import Bot

from twidi.admin.models import Configuration


class PubSubHandler:
    redemptions = []

    def __init__(self, bot: Bot, config: Configuration):
        self.bot = bot
        client = twitchio.Client(token=config.bot_client_token)
        client.pubsub = pubsub.PubSubPool(client)
        self.update_redemptions()

        @client.event()
        async def event_pubsub_points_message(event: pubsub.PubSubChannelPointsMessage):
            print('Received redemption', event.__str__())

        async def main():
            topics = [
                pubsub.channel_points(config.broadcaster_access_token)[config.channel_id],
            ]
            await client.pubsub.subscribe_topics(topics)
            await client.start()

        client.loop.run_until_complete(main())

    def update_redemptions(self):
        for name, command in self.bot.commands.items():
            if command.point_redemption:
                self.redemptions.append(command)

import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore


async def on_event(partition_context, event):
    # Print the event data.
    print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'), partition_context.partition_id))

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)

async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string("DefaultEndpointsProtocol=https;AccountName=eventhublab;AccountKey=c2djYUaXQDRvz+woOOeQdYrBTwm4jXkz7EXETJ9Fr6sHLMO+VfRqFKiYou1Bp/47Khcxi3BxY6sKsTyKC29CPw==;EndpointSuffix=core.windows.net", "offset")

    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string("Endpoint=sb://eventhublab.servicebus.windows.net/;SharedAccessKeyName=recv;SharedAccessKey=6yJCo5yI2PyNXwmHqCcles+wWlEmxwJFTOuJH71LHG8=;EntityPath=demo-eventhub", consumer_group="$Default", eventhub_name="demo-eventhub", checkpoint_store=checkpoint_store)
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event,  starting_position="-1")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())
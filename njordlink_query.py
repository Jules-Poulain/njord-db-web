import os
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

async def get_latest_pgns():
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=os.getenv("API_KEY_SECRET"),
        ),
        auth_entity=os.getenv("API_KEY_ID"),
    )

    print("Creating client...")
    viam_client = await ViamClient.create_from_dial_options(dial_options)
    print("Client created:", viam_client)

    try:
        print("Getting data client...")
        data_client = viam_client.data_client
        print("Data client:", data_client)

        print("Running query...")
        records = await data_client.tabular_data_by_sql(
            organization_id=os.getenv("ORG_ID"),
            sql_query="""
            SELECT * FROM readings
            ORDER BY time_received DESC
            LIMIT 1
            """,
        )

        print("Records:", records)

        if not records:
            return None

        return records[0].data

    finally:
        print("Closing client...")
        await viam_client.close()
        print("Closed.")
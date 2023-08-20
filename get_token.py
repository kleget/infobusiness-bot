from yoomoney import Authorize

Authorize(
      client_id="8C0A9AC8BF8AA1D914E72BF8A9B51A97FAD0BFB427DF1A2661C7448EA335A60F",
      redirect_uri="https://t.me/audioaptechka_bot",
      scope=["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
      )


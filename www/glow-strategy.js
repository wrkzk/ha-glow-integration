class GlowStrategy {
    static async generate(config, hass) {
        var all_cards = [
            {
                "type": "custom:spacer-card"
            },
            {
                "type": "custom:title-card"
            },
            {
                "type": "custom:spacer-card"
            },
            {
                "type": "custom:carbon-card"
            },
            {
                "type": "custom:power-card"
            },
            {
                "type": "custom:chartjs-card"
            },
            {
                "type": "custom:price-card"
            },
            {
                "type": "custom:consumption-card"
            },
        ]

        var entities = await Promise.all([
            hass.callWS({ type: "config/entity_registry/list" })
        ]);

        var j = 1;
        for (let i = 0; i < entities[0].length; ++i) {
            if (entities[0][i].entity_id.length >= 26) {
                if (entities[0][i].entity_id.substring(7, 26) === "current_temperature") {
                    all_cards.push({
                        "type": "custom:thermal-card",
                        "sensor": j
                    })
                    ++j;
                }
            }
        }

        console.log(all_cards)

        return {
            title: "Generated Glow Dashboard",
            views: [
                {
                    "cards": all_cards
                }
            ]
        };
    }
}

customElements.define("ll-strategy-dashboard-glow", GlowStrategy)
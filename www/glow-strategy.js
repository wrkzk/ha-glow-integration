class GlowStrategy {
    static async generate(hass, config) {
        return {
            title: "Generated Glow Dashboard",
            views: [
                {
                    "cards": [
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
                            "type": "custom:consumption-card"
                        },
                        {
                            "type": "custom:chartjs-card"
                        },
                        {
                            "type": "custom:price-card"
                        },
                        {
                            "type": "custom:power-card"
                        }
                    ]
                }
            ]
        };
    }
}

customElements.define("ll-strategy-dashboard-glow", GlowStrategy)
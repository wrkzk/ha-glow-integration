class GlowStrategy {
    static async generate(hass, config) {
        return {
            title: "Generated Glow Dashboard",
            views: [
                {
                    "cards": [
                        {
                            "type": "markdown",
                            "content": `This is test content`
                        },
                        {
                            "type": "custom:carbon-card"
                        },
                        {
                            "type": "custom:consumption-card"
                        },
                        {
                            "type": "custom:chartjs-card"
                        }
                    ]
                }
            ]
        };
    }
}

customElements.define("ll-strategy-dashboard-glow", GlowStrategy)
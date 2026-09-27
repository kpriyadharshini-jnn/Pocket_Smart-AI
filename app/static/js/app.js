async function api(url, options = {}) {

    const response = await fetch(
        url,
        {
            credentials: "same-origin",
            ...options
        }
    );


    const contentType =
        response.headers.get(
            "content-type"
        ) || "";


    const data =
        contentType.includes(
            "application/json"
        )
            ? await response.json()
            : await response.text();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            data.message ||
            "Request failed"
        );

    }


    return data;
}



function formObject(form) {

    const data =
        new FormData(form);

    return Object.fromEntries(
        data.entries()
    );
}



window.initAuthForm =
function (
    id,
    url,
    redirect
) {

    const form =
        document.getElementById(id);


    if (!form) return;


    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const message =
                document.getElementById(
                    "formMessage"
                );


            message.textContent =
                "Please wait...";


            try {

                await api(
                    url,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                formObject(form)
                            )
                    }
                );


                if (
                    url.endsWith(
                        "/register"
                    )
                ) {

                    message.textContent =
                        "Registration complete.";

                    setTimeout(
                        function () {

                            location.href =
                                redirect;

                        },
                        500
                    );

                } else {

                    location.href =
                        redirect;
                }


            } catch (error) {

                message.textContent =
                    error.message;
            }

        }
    );
};



document
    .getElementById("logoutBtn")
    ?.addEventListener(
        "click",
        async function () {

            await api(
                "/api/auth/logout",
                {
                    method: "POST"
                }
            );

            location.href = "/";

        }
    );



function parseItems(text) {

    const items = {};


    (text || "")
        .split(",")
        .forEach(
            function (part) {

                const parts =
                    part.split(":");


                const name =
                    parts[0]?.trim();


                const quantity =
                    parseInt(
                        parts[1]?.trim() ||
                        "1",
                        10
                    );


                if (name) {

                    items[name] =
                        Math.max(
                            1,
                            quantity || 1
                        );
                }

            }
        );


    return items;
}



function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        function (character) {

            const entities = {

                "&": "&amp;",

                "<": "&lt;",

                ">": "&gt;",

                '"': "&quot;",

                "'": "&#39;"
            };


            return entities[
                character
            ];

        }
    );
}



function escapeAttr(value) {

    return escapeHtml(value);
}



function renderResult(
    data,
    target
) {

    const element =
        document.getElementById(
            target
        );


    const recommendations =
        (
            data.recommendations ||
            []
        )
        .map(
            function (item) {

                return `

                <article class="rec-card">

                    <div class="rec-top">

                        <div>

                            <h3>
                                ${escapeHtml(item.name)}
                            </h3>

                            <span class="pill">

                                ${escapeHtml(
                                    item.platform
                                )}

                                ·

                                ${escapeHtml(
                                    item.category
                                )}

                            </span>

                        </div>


                        <strong>

                            ₹${Number(
                                item.estimated_price
                            ).toLocaleString(
                                "en-IN"
                            )}

                        </strong>

                    </div>


                    <p>

                        ${escapeHtml(
                            item.reason || ""
                        )}

                    </p>


                    ${
                        item.link

                        ? `

                        <a
                            href="${escapeAttr(
                                item.link
                            )}"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Open Platform Search →
                        </a>

                        `

                        : ""
                    }

                </article>

                `;

            }
        )
        .join("");


    const allocations =
        Object.entries(
            data.allocations || {}
        )
        .map(
            function ([key, value]) {

                return `

                <span class="pill">

                    ${escapeHtml(key)}:

                    ₹${Number(
                        value
                    ).toLocaleString(
                        "en-IN"
                    )}

                </span>

                `;

            }
        )
        .join(" ");


    element.innerHTML = `

        <div class="result">

            <p class="eyebrow">

                ${escapeHtml(
                    data.source_mode ||
                    "PLAN"
                ).toUpperCase()}

            </p>


            <h2>

                ${escapeHtml(
                    data.title
                )}

            </h2>


            <p class="summary">

                ${escapeHtml(
                    data.summary
                )}

            </p>


            <div class="metrics">


                <div class="metric">

                    <small>
                        Budget
                    </small>

                    <strong>

                        ₹${Number(
                            data.budget
                        ).toLocaleString(
                            "en-IN"
                        )}

                    </strong>

                </div>


                <div class="metric">

                    <small>
                        Estimated Total
                    </small>

                    <strong>

                        ₹${Number(
                            data.estimated_total
                        ).toLocaleString(
                            "en-IN"
                        )}

                    </strong>

                </div>


                <div class="metric">

                    <small>
                        Remaining
                    </small>

                    <strong>

                        ₹${Number(
                            data.budget_remaining
                        ).toLocaleString(
                            "en-IN"
                        )}

                    </strong>

                </div>


            </div>


            <h3>
                Budget Allocation
            </h3>


            <p>
                ${allocations}
            </p>


            <h3>
                Recommendations
            </h3>


            <div class="recommendations">

                ${
                    recommendations ||
                    "<p>No recommendations returned.</p>"
                }

            </div>


            <h3>
                Tips
            </h3>


            <ul>

                ${
                    (data.tips || [])
                    .map(
                        function (tip) {

                            return `

                            <li>

                                ${escapeHtml(
                                    tip
                                )}

                            </li>

                            `;

                        }
                    )
                    .join("")
                }

            </ul>


        </div>

    `;
}



window.initHomePlanner =
function (
    formId,
    target
) {

    const form =
        document.getElementById(
            formId
        );


    if (!form) return;


    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const raw =
                formObject(form);


            const payload = {

                budget:
                    Number(
                        raw.budget
                    ),

                rooms:
                    raw.rooms
                        .split(",")
                        .map(
                            x => x.trim()
                        )
                        .filter(Boolean),

                style:
                    raw.style,

                items:
                    parseItems(
                        raw.items
                    ),

                notes:
                    raw.notes
            };


            document.getElementById(
                target
            ).innerHTML = `

                <div class="empty-state">

                    Generating your plan...

                </div>

            `;


            try {

                const result =
                    await api(
                        "/api/generate-home",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )
                        }
                    );


                renderResult(
                    result,
                    target
                );


            } catch (error) {

                document.getElementById(
                    target
                ).innerHTML = `

                    <p class="message">

                        ${escapeHtml(
                            error.message
                        )}

                    </p>

                `;
            }

        }
    );
};



window.initPartyPlanner =
function (
    formId,
    target
) {

    const form =
        document.getElementById(
            formId
        );


    if (!form) return;


    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const raw =
                formObject(form);


            const payload = {

                budget:
                    Number(
                        raw.budget
                    ),

                guests:
                    Number(
                        raw.guests
                    ),

                event_type:
                    raw.event_type,

                venue:
                    raw.venue,

                city:
                    raw.city,

                preferences:
                    raw.preferences
            };


            document.getElementById(
                target
            ).innerHTML = `

                <div class="empty-state">

                    Generating your party plan...

                </div>

            `;


            try {

                const result =
                    await api(
                        "/api/generate-party",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    payload
                                )
                        }
                    );


                renderResult(
                    result,
                    target
                );


            } catch (error) {

                document.getElementById(
                    target
                ).innerHTML = `

                    <p class="message">

                        ${escapeHtml(
                            error.message
                        )}

                    </p>

                `;
            }

        }
    );
};



window.initJewelryPlanner =
function (
    formId,
    target
) {

    const form =
        document.getElementById(
            formId
        );


    if (!form) return;


    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const formData =
                new FormData(form);


            document.getElementById(
                target
            ).innerHTML = `

                <div class="empty-state">

                    Analyzing your jewelry plan...

                </div>

            `;


            try {

                const result =
                    await api(
                        "/api/generate-jewelry",
                        {
                            method: "POST",

                            body:
                                formData
                        }
                    );


                renderResult(
                    result,
                    target
                );


            } catch (error) {

                document.getElementById(
                    target
                ).innerHTML = `

                    <p class="message">

                        ${escapeHtml(
                            error.message
                        )}

                    </p>

                `;
            }

        }
    );
};



window.loadHistory =
async function (
    targetId
) {

    const target =
        document.getElementById(
            targetId
        );


    try {

        const data =
            await api(
                "/api/history"
            );


        if (!data.length) {

            target.innerHTML =
                "<p>No plans yet.</p>";

            return;
        }


        target.innerHTML =
            data.map(
                function (item) {

                    return `

                    <article class="history-card">

                        <strong>

                            ${escapeHtml(
                                item.response.title
                            )}

                        </strong>


                        <div>

                            ${escapeHtml(
                                item.planner_type
                            )}

                            ·

                            ${new Date(
                                item.created_at
                            ).toLocaleString()}

                            ·

                            ₹${Number(
                                item.response.budget
                            ).toLocaleString(
                                "en-IN"
                            )}

                        </div>


                        <p>

                            ${escapeHtml(
                                item.response.summary
                            )}

                        </p>

                    </article>

                    `;

                }
            ).join("");


    } catch (error) {

        target.innerHTML = `

            <p class="message">

                ${escapeHtml(
                    error.message
                )}

            </p>

        `;
    }
};



window.loadRecentHistory =
async function (
    targetId
) {

    const target =
        document.getElementById(
            targetId
        );


    try {

        const data =
            await api(
                "/api/history"
            );


        if (!data.length) {

            target.innerHTML =
                "<p>No plans yet. Start planning!</p>";

            return;
        }


        target.innerHTML =
            data
                .slice(0, 5)
                .map(
                    function (item) {

                        return `

                        <div class="history-card">

                            <strong>

                                ${escapeHtml(
                                    item.response.title
                                )}

                            </strong>


                            <div>

                                ${new Date(
                                    item.created_at
                                ).toLocaleString()}

                            </div>

                        </div>

                        `;

                    }
                )
                .join("");


    } catch (error) {

        target.innerHTML = `

            <p>

                ${escapeHtml(
                    error.message
                )}

            </p>

        `;
    }
};
let stripe;
fetch("/config/")
    .then((result) => { return result.json() })
    .then((data) => {
        stripe = Stripe(data.publicKey)
        console.log(stripe)
    })

function getSession() {
    fetch("/create-checkout-session/")
        .then((result) => { return result.json(); })
        .then((data) => {
            console.log(data);
            return stripe.redirectToCheckout({ sessionId: data.sessionId })
        })
}


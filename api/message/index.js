module.exports = async function (context, req) {
    context.res.json({
        text: "Hello from the API. If you are seeing this than our API is working as intended."
    });
};
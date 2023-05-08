"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.rotateWithBrightData = void 0;
const request_promise_1 = __importDefault(require("request-promise"));
async function rotateWithBrightData(url) {
    console.log('URL=>', url);
    // const url = 'https://www.phin.org.uk/search/consultants?s_location_input=London&s_location_coordinates=51.5072178%2C-0.1275862&s_speciality_input=General%20medicine&s_speciality_id=300';
    const options = {
        url: url,
        proxy: `http://${process.env.luminatiUsername}-session-rand${Math.ceil(Math.random() * 10000000)}:${process.env.luminatiPassword}@zproxy.lum-superproxy.io:22225`,
        rejectUnauthorized: false
    };
    const data = await (0, request_promise_1.default)(options);
    return data;
}
exports.rotateWithBrightData = rotateWithBrightData;
//# sourceMappingURL=rotateWithBrightData.js.map
import dotenv from 'dotenv';
import express from 'express';
import * as parse5 from 'parse5';
import { rotateWithBrightData } from './rotateWithBrightData';
const fs = require('fs');

dotenv.config();

const app = express();
const port = 3000;
const parsedData = [];
const foundEmails = new Set();
const foundPhones = new Set();
let counter = 1;

// (async () => {
//     const url = 'https://www.example.com';
//     const data = await rotateWithBrightData(url);
//     console.log(data);
// })();

app.get('/', async (req, res) => {
    try {
        let page = 1;
        const lastPage = 21;
        let url = `https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber=${page}`;
        let data = await rotateWithBrightData(url);
        const hrefs = [];
        const document = parse5.parse(data);

        const findHref = (node) => {
            if (node.tagName === 'a') {
                const href = node.attrs.find((attr) => attr.name === 'href');
                const viewLinknAttr = node.attrs.find((attr) => attr.name === 'class' && attr.value.includes('docresults'));
                if (href && viewLinknAttr) {
                    const fullHref = `https://www.idf.co.uk${href.value}`;
                    // hrefs.push(href.value);
                    console.log(href.value);
                }
            }
            if (node.childNodes) {
                node.childNodes.forEach((childNode) => findHref(childNode));
            }
        };

        const findData = (node) => {
            const mainContentDiv = findDivWithClass(node, 'main-content svelte-ectbpk');
            const title = findFirstH1(mainContentDiv);
            const mainContentDivAbout = findDivWithClass(node, 'body-section svelte-1cjckml');
            const contentContainerDiv = findDivWithClass(mainContentDivAbout, 'content-container svelte-1cjckml');
            const subSpecialities = findSubSpecialities(contentContainerDiv);

            const email = findEmail(node, 'center svelte-11uoyco');
            const phone = findPhone(node, 'center svelte-11uoyco');

            // parsedData.push(`${counter},${title},${subSpecialities},${email},${phone}`);

            console.log(parsedData);
            counter++;
        }

        const findDivWithClass = (node, className) => {
            if (node && node.nodeName === 'div' &&
                node.attrs &&
                node.attrs.some(attr => attr.name === 'class' && attr.value === className)) {
                return node;
            }

            if (node && node.childNodes) {
                for (const childNode of node.childNodes) {
                    const result = findDivWithClass(childNode, className);
                    if (result) {
                        console.log('div with class found:', result);
                        return result;
                    }
                }
            }

            console.log('div with class not found');
            return null;
        }

        const findFirstH1 = (node) => {
            if (node.nodeName === 'h1') {
                const name = node.childNodes.find((childNode) => childNode.nodeName === '#text').value.trim();
                console.log('Name=>', name);
                return name;
            }

            if (node.childNodes) {
                return findFirstH1(node.childNodes[0]);
            }

            return null;
        }

        const findSubSpecialities = (node) => {
            let result = '';
            if (node.nodeName === 'p' &&
                node.attrs &&
                node.attrs.some(attr => attr.name === 'id' && attr.value === 'profile-about-sub-specialities')) {
                node.childNodes.forEach(childNode => {
                    if (childNode.nodeName === '#text') {
                        result = childNode.value || childNode.nodeValue;
                    }
                });
                return result;
            }

            if (node && node.childNodes) {
                for (const childNode of node.childNodes) {
                    const result = findSubSpecialities(childNode);
                    if (result) {
                        return result;
                    }
                }
            }
            return null;
        }

        const findEmail = (node, className) => {
            if (node.nodeName === 'a' &&
                node.attrs &&
                node.attrs.some(attr => attr.name === 'href' && attr.value.startsWith('mailto:'))) {
                return node.attrs.find(attr => attr.name === 'href').value.slice(7).split('?')[0];
            }

            if (node.childNodes) {
                for (const childNode of node.childNodes) {
                    const result = findEmail(childNode, className);
                    if (result) {
                        return result;
                    }
                }
            }

            return null;
        }

        const findPhone = (node, className) => {
            if (node.nodeName === 'a' &&
                node.attrs &&
                node.attrs.some(attr => attr.name === 'href' && attr.value.startsWith('tel:'))) {
                return node.attrs.find(attr => attr.name === 'href').value.slice(4);
            }

            if (node.childNodes) {
                for (const childNode of node.childNodes) {
                    const result = findPhone(childNode, className);
                    if (result) {
                        return result;
                    }
                }
            }

            return null;
        }

        findHref(document);

        // while (page <= 1) {
        //     while (hrefs.length != 0) {
        //         const nextUrl = `https://www.phin.org.uk/${hrefs.shift()}`;
        //         console.log('PAGE=>', page, 'NEXTURL=>', nextUrl);
        //         const dataNext = await rotateWithBrightData(nextUrl);
        //         const documentNext = parse5.parse(dataNext);
        //         findData(documentNext);
        //     }
        //     page++;
        //     const nextPageUrl = url + `&s_page_number=${page}`;
        //     data = await rotateWithBrightData(nextPageUrl);
        //     const nextPageData = parse5.parse(data);
        //     findHref(nextPageData);
        // }

        // Convert parsedData array to CSV format and write to file
        const csvData = parsedData.map((data) => {
            return data.join(',') + '\n';
        }).join("");

        fs.writeFile('file.csv', csvData, (err) => {
            if (err) throw err;
            console.log('Data has been written to file');
        });
        res.send('Data parsed successfully');
    } catch (err) {
        console.error(err);
        res.status(500).send('Server error');
    }
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});

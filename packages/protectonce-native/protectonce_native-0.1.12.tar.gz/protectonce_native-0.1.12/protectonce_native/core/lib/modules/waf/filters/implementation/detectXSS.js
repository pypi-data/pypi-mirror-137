const BaseFilter = require("../base")
var poNative = require('@protectonce/native');

class DetectXSSFilter extends BaseFilter {
    constructor(filterDef) {
        super(filterDef, "detectXSS");
    }

    doCheckCB(data, originalData, findingCb, doneCb) {
        let match = poNative.detectXSS(data);
        if (match) {
            findingCb({
                data,
                originalData,
                pattern: this.pattern
            });
        }
        doneCb();
    }
};

module.exports = DetectXSSFilter;
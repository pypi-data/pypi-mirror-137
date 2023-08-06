"use strict";
(self["webpackChunkjupyterlab_kernel_usage"] = self["webpackChunkjupyterlab_kernel_usage"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-132265"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab_kernel_usage', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./panel */ "./lib/panel.js");





var CommandIDs;
(function (CommandIDs) {
    CommandIDs.getKernelUsage = 'kernel-usage:get';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the kernelusage extension.
 */
const plugin = {
    id: 'kernelusage:plugin',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher],
    autoStart: true,
    activate: (app, palette, notebookTracker, launcher) => {
        const { commands, shell } = app;
        const category = 'Kernel Resource';
        if (launcher) {
            launcher.add({
                command: CommandIDs.getKernelUsage,
                category: category
            });
        }
        async function createPanel() {
            const panel = new _panel__WEBPACK_IMPORTED_MODULE_4__.KernelUsagePanel({
                widgetAdded: notebookTracker.widgetAdded,
                currentNotebookChanged: notebookTracker.currentChanged
            });
            shell.add(panel, 'right', { rank: 200 });
            return panel;
        }
        commands.addCommand(CommandIDs.getKernelUsage, {
            label: 'Kernel Usage',
            caption: 'Kernel Usage',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.jupyterIcon,
            execute: createPanel
        });
        palette.addItem({ command: CommandIDs.getKernelUsage, category });
        createPanel();
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/panel.js":
/*!**********************!*\
  !*** ./lib/panel.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelUsagePanel": () => (/* binding */ KernelUsagePanel)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);



const PANEL_CLASS = 'jp-kernelusage-view';
class KernelUsagePanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.StackedPanel {
    constructor(props) {
        super();
        this.addClass(PANEL_CLASS);
        this.id = 'kernelusage-panel-id';
        this.title.caption = 'Kernel Usage';
        this.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.jupyterIcon;
        this.title.closable = true;
        const widget = new _widget__WEBPACK_IMPORTED_MODULE_2__.KernelUsageWidget({
            widgetAdded: props.widgetAdded,
            currentNotebookChanged: props.currentNotebookChanged
        });
        this.addWidget(widget);
    }
    dispose() {
        super.dispose();
    }
    onCloseRequest(msg) {
        super.onCloseRequest(msg);
        this.dispose();
    }
}


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelUsageWidget": () => (/* binding */ KernelUsageWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/polling */ "./node_modules/@lumino/polling/dist/index.es6.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");




const UNKONWN_USAGE = {
    kernel_cpu: -1,
    kernel_memory: -1,
    host_cpu_percent: -1,
    host_virtual_memory: {
        active: -1,
        available: -1,
        free: -1,
        inactive: -1,
        percent: -1,
        total: -1,
        used: -1,
        wired: -1
    }
};
const POLL_INTERVAL_SEC = 5;
const POLL_MAX_INTERVAL_SEC = 300;
const kernelPools = new Map();
const getUsage = (kernelId) => {
    const kernelPoll = kernelPools.get(kernelId);
    if (kernelPoll) {
        return kernelPoll.usage;
    }
    return UNKONWN_USAGE;
};
const KernelUsage = (props) => {
    const [kernelId, setKernelId] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)();
    const requestUsage = async (kernelId) => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)(`get_usage/${kernelId}`)
            .then(data => {
            const kernelPoll = kernelPools.get(kernelId);
            if (kernelPoll) {
                kernelPoll.usage = data.content;
                kernelPools.set(kernelId, kernelPoll);
            }
        })
            .catch(reason => {
            console.error(`The kernelusage server extension has returned an error.\n${reason}`);
            const kernelPoll = kernelPools.get(kernelId);
            kernelPoll === null || kernelPoll === void 0 ? void 0 : kernelPoll.poll.stop().then(() => {
                kernelPools.delete(kernelId);
            });
        });
    };
    const doPoll = (kernelId) => {
        let kernelPoll = kernelPools.get(kernelId);
        if (!kernelPoll) {
            const poll = new _lumino_polling__WEBPACK_IMPORTED_MODULE_1__.Poll({
                auto: true,
                factory: () => requestUsage(kernelId),
                frequency: {
                    interval: POLL_INTERVAL_SEC * 1000,
                    backoff: true,
                    max: POLL_MAX_INTERVAL_SEC * 1000
                },
                name: `@jupyterlab/kernel:KernelUsage#${kernelId}`,
                standby: 'when-hidden'
            });
            kernelPoll = {
                poll,
                usage: UNKONWN_USAGE
            };
            kernelPools.set(kernelId, kernelPoll);
        }
    };
    props.currentNotebookChanged.connect((sender, panel) => {
        var _a, _b, _c, _d, _e;
        panel === null || panel === void 0 ? void 0 : panel.sessionContext.kernelChanged.connect((_sender, args) => {
            var _a;
            const kernelId = (_a = args.newValue) === null || _a === void 0 ? void 0 : _a.id;
            setKernelId(kernelId);
            doPoll(kernelId);
        });
        if (((_a = panel === null || panel === void 0 ? void 0 : panel.sessionContext.session) === null || _a === void 0 ? void 0 : _a.id) !== kernelId) {
            if ((_c = (_b = panel === null || panel === void 0 ? void 0 : panel.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.id) {
                const kernelId = (_e = (_d = panel === null || panel === void 0 ? void 0 : panel.sessionContext.session) === null || _d === void 0 ? void 0 : _d.kernel) === null || _e === void 0 ? void 0 : _e.id;
                setKernelId(kernelId);
                doPoll(kernelId);
            }
        }
    });
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", { className: "jp-kernelusage-separator" }, "Kernel Usage"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Kernel ID: ",
            kernelId),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "CPU: ",
            kernelId && getUsage(kernelId).kernel_cpu),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Memory: ",
            kernelId && getUsage(kernelId).kernel_memory),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("hr", null),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h4", { className: "jp-kernelusage-separator" }, "Host CPU"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Percentage ",
            kernelId && getUsage(kernelId).host_cpu_percent),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h4", { className: "jp-kernelusage-separator" }, "Host Virtual Memory"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Active: ",
            kernelId && getUsage(kernelId).host_virtual_memory.active),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Available:",
            ' ',
            kernelId && getUsage(kernelId).host_virtual_memory.available),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Free: ",
            kernelId && getUsage(kernelId).host_virtual_memory.free),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Inactive: ",
            kernelId && getUsage(kernelId).host_virtual_memory.inactive),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Percent: ",
            kernelId && getUsage(kernelId).host_virtual_memory.percent),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Total: ",
            kernelId && getUsage(kernelId).host_virtual_memory.total),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Used: ",
            kernelId && getUsage(kernelId).host_virtual_memory.used),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
            "Wired: ",
            kernelId && getUsage(kernelId).host_virtual_memory.wired)));
};
class KernelUsageWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    constructor(props) {
        super();
        this._widgetAdded = props.widgetAdded;
        this._currentNotebookChanged = props.currentNotebookChanged;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(KernelUsage, { widgetAdded: this._widgetAdded, currentNotebookChanged: this._currentNotebookChanged }));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-132265.e27cd975629bcb477394.js.map
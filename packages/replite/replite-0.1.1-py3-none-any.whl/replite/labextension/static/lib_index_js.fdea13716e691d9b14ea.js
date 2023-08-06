"use strict";
(self["webpackChunkreplite"] = self["webpackChunkreplite"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlite_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlite/ui-components */ "webpack/sharing/consume/default/@jupyterlite/ui-components/@jupyterlite/ui-components");
/* harmony import */ var _jupyterlite_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlite_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_5__);






/**
 * A plugin to add buttons to the console toolbar.
 */
const buttons = {
    id: 'replite:buttons',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator],
    optional: [_jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__.IConsoleTracker],
    activate: (app, translator, tracker) => {
        if (!tracker) {
            return;
        }
        const { commands } = app;
        const trans = translator.load('retrolab');
        // wrapper commands to be able to override the icon
        const runCommand = 'replite:run';
        commands.addCommand(runCommand, {
            caption: trans.__('Run'),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.runIcon,
            execute: () => {
                return commands.execute('console:run-forced');
            }
        });
        const runButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.CommandToolbarButton({
            commands,
            id: runCommand
        });
        const restartCommand = 'replite:restart';
        commands.addCommand(restartCommand, {
            caption: trans.__('Restart'),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.refreshIcon,
            execute: () => {
                return commands.execute('console:restart-kernel');
            }
        });
        const restartButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.CommandToolbarButton({
            commands,
            id: restartCommand
        });
        const clearCommand = 'replite:clear';
        commands.addCommand(clearCommand, {
            caption: trans.__('Clear'),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.clearIcon,
            execute: () => {
                return commands.execute('console:clear');
            }
        });
        const clearButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.CommandToolbarButton({
            commands,
            id: clearCommand
        });
        tracker.widgetAdded.connect((_, console) => {
            const { toolbar } = console;
            console.toolbar.addItem('run', runButton);
            console.toolbar.addItem('restart', restartButton);
            console.toolbar.addItem('clear', clearButton);
            toolbar.addItem('spacer', _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar.createSpacerItem());
            const wrapper = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Panel();
            wrapper.addClass('jp-PoweredBy');
            const node = document.createElement('a');
            node.textContent = trans.__('Powered by JupyterLite');
            node.href = 'https://github.com/jupyterlite/jupyterlite';
            node.target = '_blank';
            node.rel = 'noopener noreferrer';
            const poweredBy = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget({ node });
            const icon = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget();
            _jupyterlite_ui_components__WEBPACK_IMPORTED_MODULE_4__.liteIcon.element({
                container: icon.node,
                elementPosition: 'center',
                margin: '2px 2px 2px 8px',
                height: 'auto',
                width: '16px'
            });
            wrapper.addWidget(poweredBy);
            wrapper.addWidget(icon);
            toolbar.addItem('powered-by', wrapper);
        });
    }
};
/**
 * A plugin to parse custom parameters from the query string arguments.
 */
const parameters = {
    id: 'replite:parameters',
    autoStart: true,
    optional: [_jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__.IConsoleTracker],
    activate: (app, tracker) => {
        if (!tracker) {
            return;
        }
        const search = window.location.search;
        const urlParams = new URLSearchParams(search);
        const code = urlParams.getAll('code');
        const kernel = urlParams.get('kernel');
        const toolbar = urlParams.get('toolbar');
        tracker.widgetAdded.connect(async (_, widget) => {
            const { console } = widget;
            // hide the first select kernel dialog if a kernel is specified
            // TODO: support specifying kernel preference in upstream RetroLab
            if (kernel) {
                const hideFirstDialog = (_, w) => {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.tracker.widgetAdded.disconnect(hideFirstDialog);
                    requestAnimationFrame(() => w.resolve(0));
                };
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.tracker.widgetAdded.connect(hideFirstDialog);
                await console.sessionContext.changeKernel({ name: kernel });
            }
            if (code) {
                await console.sessionContext.ready;
                code.forEach(line => console.inject(line));
            }
            if (!toolbar) {
                // hide the toolbar by default if not specified
                widget.toolbar.dispose();
            }
        });
    }
};
const plugins = [buttons, parameters];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.fdea13716e691d9b14ea.js.map
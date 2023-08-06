"use strict";
(self["webpackChunk_tigergraph_mlworkbench"] = self["webpackChunk_tigergraph_mlworkbench"] || []).push([["lib_index_js"],{

/***/ "./lib/ServerController.js":
/*!*********************************!*\
  !*** ./lib/ServerController.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ServerController": () => (/* binding */ ServerController)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _ServerDetailForm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./ServerDetailForm */ "./lib/ServerDetailForm.js");
/* harmony import */ var _gdps__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./gdps */ "./lib/gdps.js");
/* harmony import */ var _database__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./database */ "./lib/database.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);





class ServerController extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.state = {
            renderView: 'default'
        };
        this.setEditingState = this.setEditingState.bind(this);
        this.updateServer = this.updateServer.bind(this);
        this.handleExit = this.handleExit.bind(this);
    }
    setEditingState(state) {
        if (state) {
            this.setState({ renderView: 'editing' });
        }
        else {
            this.setState({ renderView: 'default' });
        }
    }
    updateServer(newServer) {
        this.props.updateServer(this.props.id, newServer);
    }
    handleExit() {
        this.setState({ renderView: 'default' });
    }
    render() {
        if (this.state.renderView === 'editing') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("fieldset", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ServerDetailForm__WEBPACK_IMPORTED_MODULE_2__.ServerDetailForm, { serverName: this.props.serverName, serverAddress: this.props.serverAddress, hostOS: this.props.hostOS, restPort: this.props.restPort, gsqlPort: this.props.gsqlPort, gdpsPort: this.props.gdpsPort, setEditingState: this.setEditingState, submitServerDetail: this.updateServer })));
        }
        else if (this.state.renderView === 'gdps') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("fieldset", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_gdps__WEBPACK_IMPORTED_MODULE_3__.GDPSController, { handleExit: this.handleExit, serverAddress: this.props.serverAddress, gdpsPort: this.props.gdpsPort, jupyterApp: this.props.jupyterApp, hostOS: this.props.hostOS })));
        }
        else if (this.state.renderView === 'database') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("fieldset", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_database__WEBPACK_IMPORTED_MODULE_4__.DBController, { handleExit: this.handleExit, serverAddress: this.props.serverAddress, restPort: this.props.restPort, gsqlPort: this.props.gsqlPort, hostOS: this.props.hostOS, jupyterApp: this.props.jupyterApp })));
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("fieldset", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("legend", null, this.props.serverName),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null,
                    this.props.serverAddress,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "btn-invisible", onClick: () => this.setState({ renderView: 'editing' }) },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.editIcon.react, { height: "14px", "margin-bottom": "-2px", "margin-left": "2px", padding: "0px" }))),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: () => this.setState({ renderView: 'database' }) }, "GraphStudio"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: () => this.setState({ renderView: 'gdps' }) }, "GDPS")));
        }
    }
}


/***/ }),

/***/ "./lib/ServerDetailForm.js":
/*!*********************************!*\
  !*** ./lib/ServerDetailForm.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ServerDetailForm": () => (/* binding */ ServerDetailForm)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

class ServerDetailForm extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCancel = this.handleCancel.bind(this);
    }
    handleSubmit(event) {
        event.preventDefault();
        const target = event.target;
        this.props.submitServerDetail({
            serverName: target.serverName.value,
            serverAddress: target.serverAddress.value.replace(/\/+$/g, ''),
            hostOS: target.hostOS.value,
            restPort: target.restPort.value,
            gsqlPort: target.gsqlPort.value,
            gdpsPort: target.gdpsPort.value
        });
        this.props.setEditingState(false);
    }
    handleCancel() {
        this.props.setEditingState(false);
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", { onSubmit: this.handleSubmit },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", null,
                "Server Name ",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { className: "bottom-margin", type: "text", name: "serverName", placeholder: "My First Server", defaultValue: this.props.serverName })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", null,
                "Server Address ",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { className: "bottom-margin", type: "text", name: "serverAddress", placeholder: "http://127.0.0.1", defaultValue: this.props.serverAddress })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", null,
                "Host OS ",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("select", { name: "hostOS", defaultValue: this.props.hostOS, className: "bottom-margin" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("option", { value: "linux" }, "linux"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("option", { value: "mac" }, "mac"))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", null,
                "REST Port ",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { className: "bottom-margin", type: "text", name: "restPort", placeholder: "9000", defaultValue: this.props.restPort })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", null,
                "GSQL Port ",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { className: "bottom-margin", type: "text", name: "gsqlPort", placeholder: "14240", defaultValue: this.props.gsqlPort })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", null,
                "GDPS Port ",
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { className: "bottom-margin", type: "text", name: "gdpsPort", placeholder: "8000", defaultValue: this.props.gdpsPort })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "submit" }, "Submit"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: this.handleCancel }, "Cancel")));
    }
}


/***/ }),

/***/ "./lib/ServerIndex.js":
/*!****************************!*\
  !*** ./lib/ServerIndex.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ServerIndex": () => (/* binding */ ServerIndex)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _ServerController__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./ServerController */ "./lib/ServerController.js");
/* harmony import */ var _ServerDetailForm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./ServerDetailForm */ "./lib/ServerDetailForm.js");



class ServerIndex extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        const servers = props.settings.get('servers')
            .composite;
        this.state = {
            isAdding: false,
            serverList: servers ? servers : []
        };
        this.handleAddServer = this.handleAddServer.bind(this);
        this.setEditingState = this.setEditingState.bind(this);
        this.pushServer = this.pushServer.bind(this);
        this.updateServer = this.updateServer.bind(this);
    }
    handleAddServer() {
        this.setState({ isAdding: true });
    }
    setEditingState(state) {
        this.setState({ isAdding: state });
    }
    pushServer(newServer) {
        const servers = [...this.state.serverList, newServer];
        this.props.settings
            .set('servers', servers)
            .then(() => {
            this.setState({ serverList: servers });
        })
            .catch(reason => {
            console.error(`Failed to update server list.\n${reason}`);
        });
    }
    updateServer(index, newServer) {
        const servers = [...this.state.serverList];
        servers[index] = newServer;
        this.props.settings
            .set('servers', servers)
            .then(() => {
            this.setState({ serverList: servers });
        })
            .catch(reason => {
            console.error(`Failed to update server list.\n${reason}`);
        });
    }
    render() {
        if (this.state.isAdding) {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ServerDetailForm__WEBPACK_IMPORTED_MODULE_1__.ServerDetailForm, { serverName: "My Server", serverAddress: "http://127.0.0.1", hostOS: "linux", restPort: "9000", gsqlPort: "14240", gdpsPort: "8000", setEditingState: this.setEditingState, submitServerDetail: this.pushServer }));
        }
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
            this.state.serverList.map((server, index) => {
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ServerController__WEBPACK_IMPORTED_MODULE_2__.ServerController, { key: index, id: index, serverName: server.serverName, serverAddress: server.serverAddress, hostOS: server.hostOS, restPort: server.restPort, gsqlPort: server.gsqlPort, gdpsPort: server.gdpsPort, jupyterApp: this.props.jupyterApp, updateServer: this.updateServer }));
            }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.handleAddServer }, "Add Server")));
    }
}


/***/ }),

/***/ "./lib/ServerManager.js":
/*!******************************!*\
  !*** ./lib/ServerManager.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ServerManager": () => (/* binding */ ServerManager)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");
/* harmony import */ var _ServerIndex__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./ServerIndex */ "./lib/ServerIndex.js");




class ServerManager extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(jupyterApp, settings) {
        super();
        this.addClass('jp-ReactWidget');
        this._jupyterApp = jupyterApp;
        this._jupyterSettings = settings;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h4", null, "TigerGraph Database Server"),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_ServerIndex__WEBPACK_IMPORTED_MODULE_3__.ServerIndex, { jupyterApp: this._jupyterApp, settings: this._jupyterSettings })));
    }
}


/***/ }),

/***/ "./lib/database.js":
/*!*************************!*\
  !*** ./lib/database.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DBController": () => (/* binding */ DBController)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

class DBController extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.state = {
            renderComponent: 'testConnection'
        };
    }
    async fetchWithTimeout(resource, timeout = 3000) {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);
        const response = await fetch(resource, {
            mode: 'no-cors',
            signal: controller.signal
        });
        clearTimeout(id);
        return response;
    }
    componentDidMount() {
        this.fetchWithTimeout(this.props.serverAddress + ':' + this.props.restPort + '/echo', 1000).then(resp => {
            window.open(this.props.serverAddress + ':' + this.props.gsqlPort);
            this.props.handleExit();
        }, error => {
            this.setState({ renderComponent: 'failedConnection' });
        });
    }
    render() {
        if (this.state.renderComponent === 'testConnection') {
            return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, "Pinging the database...");
        }
        else if (this.state.renderComponent === 'failedConnection') {
            if (this.props.hostOS === 'linux') {
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Failed to reach database. Would you like to (re)install it to the server?"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: () => this.setState({ renderComponent: 'dbInstaller' }) }, "Yes"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.props.handleExit }, "No")));
            }
            else {
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null,
                        "Failed to reach database. Please check its status manually. If you haven't installed the database, try deploying a docker container to the server following the",
                        ' ',
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { href: "https://docs.tigergraph.com/tigergraph-server/current/getting-started/docker", target: "_blank" }, "official guide"),
                        "."),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.props.handleExit }, "Back")));
            }
        }
        else if (this.state.renderComponent === 'dbInstaller') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(DBInstaller, { handleExit: this.props.handleExit, hostOS: this.props.hostOS, serverAddress: this.props.serverAddress, jupyterApp: this.props.jupyterApp }));
        }
        else {
            return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, "Something went wrong. Please reload.");
        }
    }
}
class DBInstaller extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        const isLocal = props.serverAddress.includes('127.0.0.1') ||
            props.serverAddress.includes('localhost')
            ? true
            : false;
        this.state = {
            renderView: isLocal ? 'toInstall' : 'ssh',
            isLocalInstall: isLocal,
            sshUsername: '',
            sshKeyfile: ''
        };
        this.handleInstall = this.handleInstall.bind(this);
        this.handleSSH = this.handleSSH.bind(this);
    }
    handleSSH(event) {
        const target = event.target;
        this.setState({
            sshUsername: target.username.value,
            sshKeyfile: target.keyfile.value,
            renderView: 'toInstall'
        });
    }
    handleInstall() {
        const host = this.state.sshUsername +
            '@' +
            this.props.serverAddress.replace('https://', '').replace('http://', '');
        const ssh = ['ssh', '-o StrictHostKeyChecking=no'];
        if (this.state.sshKeyfile) {
            ssh.push('-i', '"' + this.state.sshKeyfile + '"');
        }
        ssh.push(host);
        const cmds = [
            'mkdir -p ~/tg_tmp;',
            'cd ~/tg_tmp;',
            'curl -O https://dl.tigergraph.com/enterprise-edition/tigergraph-3.4.0-offline.tar.gz;',
            'tar xzf tigergraph-3.4.0-offline.tar.gz;',
            'cd tigergraph-3.4.0-offline;',
            'sudo ./install.sh -n ;',
            'cd;',
            'rm -rf tg_tmp;',
            'echo; echo; echo; echo Installation finished.'
        ];
        this.setState({ renderView: 'installing' });
        const exec = this.state.isLocalInstall
            ? cmds.join(' ') + '\n'
            : ssh.join(' ') + ' "' + cmds.join(' ') + '"' + '\n';
        const commands = this.props.jupyterApp.commands;
        commands.execute('terminal:create-new').then(model => {
            const terminal = model.content;
            try {
                terminal.session.send({
                    type: 'stdin',
                    content: [exec]
                });
            }
            catch (e) {
                console.error(e);
                model.dispose();
            }
        });
    }
    render() {
        if (this.state.renderView === 'ssh') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", { onSubmit: this.handleSSH },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "We will use SSH to install the database onto the server. Please provide your SSH credentials. `sudo` access is required. If using password for SSH, leave the private key blank and you will be prompted to enter password next on the terminal."),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", name: "username", placeholder: "username" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", name: "keyfile", placeholder: "path to key file" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "submit" }, "Next")));
        }
        else if (this.state.renderView === 'toInstall') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "A terminal will open on the right and install the database to the server. Continue?"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.handleInstall }, "Yes!"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.props.handleExit }, "hmm, maybe later")));
        }
        else if (this.state.renderView === 'installing') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Installing Tigergraph database. See the terminal on the right for progress."),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.props.handleExit }, "Close")));
        }
        else {
            return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, "Something went wrong. Please reload.");
        }
    }
}


/***/ }),

/***/ "./lib/gdps.js":
/*!*********************!*\
  !*** ./lib/gdps.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GDPSController": () => (/* binding */ GDPSController)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

class GDPSController extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.state = {
            renderView: 'testConnection'
        };
    }
    async fetchWithTimeout(resource, timeout = 3000) {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);
        const response = await fetch(resource, {
            signal: controller.signal
        });
        clearTimeout(id);
        return response;
    }
    componentDidMount() {
        this.fetchWithTimeout(this.props.serverAddress + ':' + this.props.gdpsPort + '/ping', 1000).then(resp => {
            if (resp.ok) {
                this.setState({ renderView: 'successConnection' });
            }
            else {
                this.setState({ renderView: 'failedConnection' });
            }
        }, error => {
            this.setState({ renderView: 'failedConnection' });
        });
    }
    render() {
        if (this.state.renderView === 'testConnection') {
            return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, "Pinging GDPS...");
        }
        else if (this.state.renderView === 'successConnection') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null,
                    "GDPS is running happily on server ",
                    this.props.serverAddress),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.props.handleExit }, "Ok")));
        }
        else if (this.state.renderView === 'failedConnection') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Failed to reach GDPS. Would you like to (re)install it to the server?"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: () => this.setState({ renderView: 'gdpsInstaller' }) }, "Yes"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.props.handleExit }, "No")));
        }
        else if (this.state.renderView === 'gdpsInstaller') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(GDPSInstaller, { handleExit: this.props.handleExit, serverAddress: this.props.serverAddress, jupyterApp: this.props.jupyterApp, hostOS: this.props.hostOS }));
        }
        else {
            return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, "Something went wrong. Please reload.");
        }
    }
}
class GDPSInstaller extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.state = {
            renderView: 'intro',
            tg_output_path: '',
            local_output_path: '',
            isLocalInstall: props.serverAddress.includes('127.0.0.1') ||
                props.serverAddress.includes('localhost')
                ? true
                : false,
            sshUsername: '',
            sshKeyfile: '',
            tg_cluster_mode: false
        };
        this.handleVolumeMount = this.handleVolumeMount.bind(this);
        this.handleTmpOutput = this.handleTmpOutput.bind(this);
        this.handleInstall = this.handleInstall.bind(this);
        this.handleSSH = this.handleSSH.bind(this);
    }
    handleVolumeMount(state) {
        this.setState(state);
        this.setState({
            renderView: this.state.isLocalInstall ? 'toInstall' : 'ssh'
        });
    }
    handleTmpOutput(state) {
        this.setState(state);
        this.setState({
            renderView: this.state.isLocalInstall ? 'toInstall' : 'ssh'
        });
    }
    handleSSH(state) {
        this.setState(state);
        this.setState({ renderView: 'toInstall' });
    }
    handleInstall() {
        const ssh = ['ssh', '-o StrictHostKeyChecking=no'];
        if (this.state.sshKeyfile) {
            ssh.push('-i', '"' + this.state.sshKeyfile + '"');
        }
        ssh.push(this.state.sshUsername +
            '@' +
            this.props.serverAddress.replace('https://', '').replace('http://', ''));
        const appName = 'start_gdps_' + this.props.hostOS;
        const timestamp = new Date(Date.now());
        const cmds = [
            'mkdir -p ~/tg_gdps/logs;',
            'cd ~/tg_gdps;',
            'curl -O https://tigergraph-public-data.s3.us-west-1.amazonaws.com/ml-workbench/gdps/' +
                appName +
                ';',
            'chmod +x ' + appName + ';',
            '{ tg_output_path=' + this.state.tg_output_path.trim(),
            'local_output_path=' + this.state.local_output_path.trim(),
            'tg_cluster_mode=' + this.state.tg_cluster_mode.toString(),
            'nohup ./' +
                appName +
                ' >> logs/' +
                timestamp.toISOString() +
                '.log 2>&1 & };',
            'echo; echo; echo; echo Installation finished.'
        ];
        this.setState({ renderView: 'installing' });
        const exec = this.state.isLocalInstall
            ? cmds.join(' ') + '\n'
            : ssh.join(' ') +
                ' "bash -i -c ' +
                "'" +
                cmds.join(' ') +
                "'" +
                '"' +
                '\n';
        const commands = this.props.jupyterApp.commands;
        commands.execute('terminal:create-new').then(model => {
            const terminal = model.content;
            try {
                terminal.session.send({
                    type: 'stdin',
                    content: [exec]
                });
            }
            catch (e) {
                console.error(e);
                model.dispose();
            }
        });
    }
    render() {
        if (this.state.renderView === 'intro') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "To install GDPS onto this server, we first need to know how the TigerGraph database is set up there."),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: () => this.setState({ renderView: 'container' }) }, "Ok")));
        }
        else if (this.state.renderView === 'container') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Is TigerGraph database running in a container?"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: () => this.setState({ renderView: 'volumeMount' }) }, "Yes"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: () => this.setState({ renderView: 'cluster' }) }, "No")));
        }
        else if (this.state.renderView === 'cluster') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Is TigerGraph database running on a single machine or a cluster?"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: () => this.setState({ tg_cluster_mode: false, renderView: 'tmpOutput' }) }, "Single"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: () => this.setState({ tg_cluster_mode: true, renderView: 'tmpOutput' }) }, "Cluster")));
        }
        else if (this.state.renderView === 'volumeMount') {
            return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(VolumeMountForm, { update: this.handleVolumeMount });
        }
        else if (this.state.renderView === 'tmpOutput') {
            return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(TmpOutputForm, { update: this.handleTmpOutput });
        }
        else if (this.state.renderView === 'ssh') {
            return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(SSHForm, { update: this.handleSSH });
        }
        else if (this.state.renderView === 'toInstall') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Thanks for providing all the information. A terminal will open on the right and install GDPS to the server. Continue?"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.handleInstall }, "Yes!"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.props.handleExit }, "hmm, maybe later")));
        }
        else if (this.state.renderView === 'installing') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Installing GDPS. See the terminal on the right for progress."),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { onClick: this.props.handleExit }, "Close")));
        }
        else {
            return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, "Something went wrong. Please reload.");
        }
    }
}
class VolumeMountForm extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleSubmit(event) {
        event.preventDefault();
        const target = event.target;
        const volumeMount = target.volumeMount.value;
        const [host_dir, container_dir] = volumeMount.split(':');
        this.props.update({
            local_output_path: host_dir.trim() + '/gdpstmp',
            tg_output_path: container_dir.trim() + '/gdpstmp'
        });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", { onSubmit: this.handleSubmit },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "What is the argument after the -v flag (volume mount) when you started the container? (This info will be used by GDPS to read output from database)"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", name: "volumeMount", placeholder: "/folder/on/host:/folder/in/container", defaultValue: "" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "submit" }, "Next")));
    }
}
class TmpOutputForm extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleSubmit(event) {
        event.preventDefault();
        const target = event.target;
        this.props.update({
            local_output_path: target.tmpOutput.value.trim(),
            tg_output_path: target.tmpOutput.value.trim()
        });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", { onSubmit: this.handleSubmit },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Where would you like the database to write temporary outputs? (Please make sure that both the database and your account have access to the folder.) If it doesn't exist, the folder will be created."),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", name: "tmpOutput", placeholder: "/home/tigergraph/tmp", defaultValue: "" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "submit" }, "Next")));
    }
}
class SSHForm extends (react__WEBPACK_IMPORTED_MODULE_0___default().Component) {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleSubmit(event) {
        event.preventDefault();
        const target = event.target;
        this.props.update({
            sshUsername: target.username.value.trim(),
            sshKeyfile: target.keyfile.value.trim()
        });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", { onSubmit: this.handleSubmit },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", null, "Finally, we will use SSH to install GDPS onto the server. Please provide your SSH credentials (no sudo needed). If using password for SSH, leave the private key blank and you will be prompted to enter password next on the terminal."),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", name: "username", placeholder: "username", defaultValue: "" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", name: "keyfile", placeholder: "path to key file", defaultValue: "" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "submit" }, "Next")));
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "tigerIcon": () => (/* binding */ tigerIcon),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _ServerManager__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./ServerManager */ "./lib/ServerManager.js");
/* harmony import */ var _tutorial__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tutorial */ "./lib/tutorial.js");
/* harmony import */ var _style_tigerIcon_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/tigerIcon.svg */ "./style/tigerIcon.svg");








const tigerIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.LabIcon({
    name: '@tigergraph/mlworkbench',
    svgstr: _style_tigerIcon_svg__WEBPACK_IMPORTED_MODULE_5__["default"]
});
const PLUGIN_ID = '@tigergraph/mlworkbench:extension';
/**
 * Initialization data for the mlworkbench extension.
 */
const plugin = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory],
    activate: (app, settings, launcher, browser) => {
        const { shell } = app;
        // Wait for the application to be restored and
        // for the settings for this plugin to be loaded
        Promise.all([app.restored, settings.load(PLUGIN_ID)])
            .then(([, setting]) => {
            // Add TG server manager
            const serverManager = new _ServerManager__WEBPACK_IMPORTED_MODULE_6__.ServerManager(app, setting);
            serverManager.id = 'tigergraph-ml-workbench';
            serverManager.title.caption = 'ML Workbench';
            serverManager.title.icon = tigerIcon;
            shell.add(serverManager, 'left');
            // Add ML Workbench tutorials
            const commandID = 'mlworkbench:tutorial';
            app.commands.addCommand(commandID, {
                caption: 'TigerGraph ML Tutorial',
                label: 'TigerGraph ML Tutorial',
                iconClass: 'jp-TemplateIcon',
                isEnabled: () => true,
                execute: args => {
                    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.showDialog)({
                        body: new _tutorial__WEBPACK_IMPORTED_MODULE_7__.MLTutorials(),
                        buttons: [
                            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.cancelButton(),
                            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_3__.Dialog.okButton({ label: 'Open' })
                        ],
                        focusNodeSelector: 'input',
                        title: 'TigerGraph ML Tutorials'
                    }).then((event) => {
                        if (event.button.label === 'Cancel') {
                            return;
                        }
                        if (event.value) {
                            fetch(event.value)
                                .then(resp => resp.json())
                                .then(content => {
                                const path = browser.defaultBrowser.model.path;
                                return new Promise(resolve => {
                                    app.commands
                                        .execute('docmanager:new-untitled', {
                                        path,
                                        type: 'notebook'
                                    })
                                        .then(model => {
                                        app.commands
                                            .execute('docmanager:open', {
                                            factory: 'Notebook',
                                            path: model.path
                                        })
                                            .then(widget => {
                                            widget.context.ready.then(() => {
                                                widget.model.fromJSON(content);
                                                resolve(widget);
                                            });
                                        });
                                    });
                                });
                            });
                        }
                    });
                }
            });
            launcher.add({
                category: 'Notebook',
                command: commandID,
                // eslint-disable-next-line max-len
                kernelIconUrl: 'data:image/png;base64,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',
                rank: 1
            });
        })
            .catch(reason => {
            console.error(`Something went wrong when starting ml workbench.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/tutorial.js":
/*!*************************!*\
  !*** ./lib/tutorial.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MLTutorials": () => (/* binding */ MLTutorials)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

const tutorialIndex = {
    basics: {
        '0_data_ingestion': {
            label: 'Data Ingestion',
            url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/0_data_ingestion.ipynb'
        },
        '1_data_processing': {
            label: 'Data Processing',
            url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/1_data_processing.ipynb'
        },
        '2_dataloaders': {
            label: 'Data loaders',
            url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/2_dataloaders.ipynb'
        },
        '3.1_graph_convolutional_network': {
            label: 'Graph Convolutional Network',
            url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/3.1_graph_convolutional_network.ipynb'
        },
        '3.2_graphSAGE': {
            label: 'GraphSAGE',
            url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/3.2_graphSAGE.ipynb'
        },
        '3.3_graph_attention_network': {
            label: 'Graph Attention Network',
            url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/3.3_graph_attention_network.ipynb'
        }
    }
};
class MLTutorials extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        const body = document.createElement('div');
        const label = document.createElement('label');
        label.textContent = 'Tutorials:';
        const tutoSelect = document.createElement('select');
        const basics = tutorialIndex.basics;
        for (const tid of Object.keys(basics)) {
            const option = document.createElement('option');
            option.label = basics[tid].label;
            option.text = basics[tid].label;
            option.value = basics[tid].url;
            tutoSelect.appendChild(option);
        }
        body.appendChild(label);
        body.appendChild(tutoSelect);
        super({ node: body });
    }
    getValue() {
        return this.inputNode.value;
    }
    get inputNode() {
        return this.node.getElementsByTagName('select')[0];
    }
}


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/tigerIcon.svg":
/*!*****************************!*\
  !*** ./style/tigerIcon.svg ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg id=\"svg\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"400\" height=\"321.6\"\n    viewBox=\"93, 57, 216, 210\">\n    <g id=\"svgg\">\n        <path id=\"path0\"\n            d=\"M205.700 57.809 C 193.287 58.042,184.499 60.453,175.089 66.207 C 173.890 66.941,173.852 66.949,171.089 67.086 C 154.233 67.923,141.695 73.245,129.316 84.819 C 127.051 86.937,94.125 123.610,94.112 124.030 C 94.105 124.223,97.799 129.447,102.320 135.640 L 110.540 146.900 110.662 150.200 C 110.985 158.946,114.423 166.204,120.949 171.916 C 124.515 175.037,131.600 179.074,131.600 177.984 C 131.600 177.596,133.392 174.539,134.660 172.764 C 142.316 162.045,155.029 154.602,166.605 154.061 C 177.547 153.549,185.917 156.407,190.878 162.347 C 192.293 164.041,192.136 164.116,193.275 161.200 C 198.294 148.346,197.780 133.390,191.873 120.428 C 189.485 115.186,194.788 120.619,199.551 128.294 C 214.421 152.253,212.663 184.711,194.502 221.500 C 188.005 234.663,179.796 247.619,171.503 257.801 C 168.772 261.155,168.552 261.681,169.333 263.002 C 170.170 264.419,170.529 264.371,177.645 261.882 C 199.257 254.321,225.165 244.239,241.350 237.089 C 300.524 210.951,318.523 179.648,297.879 138.779 C 296.092 135.242,295.740 134.756,295.027 134.839 L 294.500 134.900 294.378 139.400 C 293.810 160.274,280.323 181.335,255.700 199.800 C 245.404 207.520,242.517 208.685,247.305 203.186 C 280.550 165.004,286.907 128.612,264.303 105.885 C 257.373 98.918,254.633 98.135,256.478 103.647 C 261.978 120.088,259.681 138.041,249.907 155.000 C 245.323 162.954,244.256 163.543,245.468 157.451 C 251.700 126.140,242.976 102.465,217.416 81.320 C 215.940 80.099,214.484 78.875,214.182 78.600 L 213.632 78.100 216.612 68.000 C 218.251 62.445,219.594 57.833,219.596 57.750 C 219.600 57.589,216.766 57.601,205.700 57.809 M164.897 91.371 C 164.015 92.225,152.563 102.675,145.700 108.890 C 143.280 111.081,141.060 113.092,140.766 113.359 C 139.712 114.316,139.815 113.624,141.244 110.147 C 142.023 108.251,143.580 104.439,144.703 101.675 C 148.383 92.621,148.593 92.466,158.700 91.310 C 161.890 90.945,164.769 90.636,165.097 90.623 L 165.694 90.600 164.897 91.371 \"\n            class=\"jp-icon3\" stroke=\"none\" fill=\"#616161\" fill-rule=\"evenodd\"></path>\n    </g>\n</svg>");

/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ })

}]);
//# sourceMappingURL=lib_index_js.ad9db91ea515a2965708.js.map
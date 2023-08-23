
# **BITO as VS Code Extension** #

<img src="../media/vscode_BITO.gif" width="900" height="500"/> <br/></br>

*<h3 style="text-align:justify">[Pick Me For Home Page](../README.md)</h3>*

## <ins>Build Extension</ins> ##


### **Step 1:** Update properties in `ui-code\package.json` as shown below ###

For Production environment

```javascript
    "build": "ng build --configuration production",
    "authwidget": "file:authwidget_prod-<latest-version>.tgz",
```

For Staging environment

```javascript
    "build": "ng build",
    "authwidget": "file:authwidget_staging-<latest-version>.tgz",
```

### **Step 2:** Modify properties in `vscode\webpack.config.js ` ###

For Production environment

```javascript
    mode: 'production'
```

For Staging environment

```javascript
    mode: 'development'
```

### **Step 3:** If required, Force install dependencies ###

For production or staging environment whenever the version of common-login (authwidget) is updated<br/>
in `ui-code\package.json ` do run command: `npm i --legacy-peer-deps --force` <br/>
to update the dependencies in local environment. 


### **Step 4:** Run build script ###

- Navigate to `vscode` as current working directory (repository) and run build script

On Windows Platform

```javascript
<your-directory>\vscode>build.bat
```

On Linux / macOS Platform (**NOTE:** the shell script needs to be updated)

```javascript
<your-directory>\vscode>build.sh
```

**<ins>NOTE:</ins>** This script will build BITO UI application and later it will build vscode extension.

<br/>

<img src="../media/important.png" width="20" height="20" /> Look for any build failure(s) or compilation issue(s).<br/>
For any error(s) fix the issue and then run again build script to create installer for vscode.


### **Step 5:** Verify the version(s) of lazy chunk files generated at the time of build creation   ###

- Compare the version(s) with the version(s) mentioned in `vscode\assets\config\application.properties` under `[Prod]` section

- If there is any chage in version(s) of lazy chunk files on command line then update the version of corresponding files in `application.properties`

- **NOTE** This change or modification is only required when the build is being created for Production environment

<img src="../media/vscode_build.png" width="800" height="400"/>



### **Step 6:** Manually install extension packaged in `.vsix` file  ###

- Option 1: Open vscode editor -> Click on Extensions Icon in the Activity Bar -> Click on View (3 dots) -> Install from VSIX..

Or, <br/>
- Option 2: Using Command Palette -> `Ctrl+Shift+P` -> Type `Install from VSIX`

- Choose the version of installer generated after running build script to install the BITO as vscode extension

- Restart vscode editor.

<br/>

<img src="../media/install_extension_vscode.gif" width="900" height="500"/>

<br/>

## Contribute ##

To contribute development work for frontend or backend application development please read the [contribution guidelines](https://bito.atlassian.net/wiki/spaces/EN/pages/209092633/Process+and+Guidelines+for+Dev+Team) first.

## License ##

Copyright (C) 2021, Bito Inc - All Rights Reserved

[Scroll to top](#bito-as-vs-code-extension)

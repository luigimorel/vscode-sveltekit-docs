'use strict';
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {

    let svelteKitDocsCreatingAProject = vscode.commands.registerCommand('extension.svelteKitDocsCreatingAProject', () => {
        vscode.commands.executeCommand('vscode.open', vscode.Uri.parse('https://kit.svelte.dev/docs/creating-a-project'));
    });
    context.subscriptions.push(svelteKitDocsCreatingAProject);

}
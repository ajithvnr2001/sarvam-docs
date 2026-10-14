---
url: https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native/
title: React Native | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:27.839424+00:00
---

# React Native | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native/

Skip to navigation

On this page

  * Install
  * Start a voice session
  * InteractionConfig
  * Callbacks
  * Custom audio interface
  * Session methods
  * Troubleshooting



Scroll to top

[SDKs](https://docs.sarvam.ai/voice-agents/deploy/sdks/python)

# React Native

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native.md "View this page as plain text")|More actions

This page is for Voice Agents.

For real-time voice on iOS and Android, the TypeScript SDK (`sarvam-conv-ai-sdk/react-native`) uses the same `ConversationAgent` client as [Web](https://docs.sarvam.ai/voice-agents/deploy/sdks/web). React Native has no built-in browser audio API, so you must pass your own `AsyncAudioInterface` for microphone capture and playback.

## Install
    
    
    npm install sarvam-conv-ai-sdk
    
    
    import { ConversationAgent } from "sarvam-conv-ai-sdk/react-native";

## Start a voice session
    
    
    import {
    
      ConversationAgent,
    
      InteractionType,
    
    } from "sarvam-conv-ai-sdk/react-native";
    
    const audioInterface = new MyRNAudioInterface();
    
    const agent = new ConversationAgent({
    
      apiKey: "your_api_key",
    
      config: {
    
        org_id: "your_org_id",
    
        workspace_id: "your_workspace_id",
    
        app_id: "your_app_id",
    
        user_identifier: "user123",
    
        user_identifier_type: "custom",
    
        interaction_type: InteractionType.CALL,
    
        input_sample_rate: 16000,
    
        output_sample_rate: 16000,
    
      },
    
      audioInterface,
    
      platform: "react-native",
    
      transcriptCallback: async (msg) => {
    
        console.log(`${msg.role}: ${msg.content}`);
    
      },
    
    });
    
    await agent.start();
    
    const connected = await agent.waitForConnect(10);
    
    if (!connected) {
    
      // Show an error or retry
    
    }

Set `platform: "react-native"` and pass an `audioInterface` that implements `AsyncAudioInterface` (see [Custom audio interface](https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native#custom-audio-interface) below).

## InteractionConfig

Field| Required| Description  
---|---|---  
`user_identifier_type`| Yes| `'custom'`, `'email'`, `'phone_number'`, or `'unknown'`  
`user_identifier`| Yes| The identifier value; also what you search by in [Log Analyser](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/log-analyser)  
`org_id`| Yes| Your organization ID  
`workspace_id`| Yes| Your workspace ID  
`app_id`| Yes| The agent to connect to  
`interaction_type`| Yes| `InteractionType.CALL` for a voice session  
`input_sample_rate`| Yes| `8000` or `16000` Hz  
`output_sample_rate`| Yes| `16000` or `22050` Hz  
`version`| No| Pins a specific committed agent version. If omitted, the SDK uses the latest committed version, and the connection fails if the agent has no committed version  
`agent_variables`| No| Seed [agent variables](https://docs.sarvam.ai/voice-agents/build/variables-personalization) at session start  
`initial_language_name`| No| Starting language; must be one of the agent’s allowed languages  
`initial_state_name`| No| Starting state, if the agent uses [states](https://docs.sarvam.ai/voice-agents/build/states-conversation-flow)  
`initial_bot_message`| No| First message from the agent  
  
## Callbacks

Pass any of these to `ConversationAgent` to react to what happens during the call:

Callback| Fires with| Use it for  
---|---|---  
`transcriptCallback`| transcript message (`role`: `Role.USER` or `Role.BOT`, `content`)| A live transcript of both sides of the call  
`audioCallback`| audio chunk| Raw agent audio, if you’re handling playback yourself  
`audioLevelCallback`| output level| Real-time level for a speaking indicator  
`eventCallback`| session event| Session events such as connect, barge-in, and end  
`stateCallback`| `AgentState`| Drive UI from `IDLE`, `CONNECTING`, `CONNECTED`, `LISTENING`, `SPEAKING`, or `ERROR`  
`startCallback`| —| Session start  
`endCallback`| —| Session end and cleanup  
  
## Custom audio interface

Implement `AsyncAudioInterface` and feed 16-bit PCM mono at the configured sample rate:
    
    
    import {
    
      AsyncAudioInterface,
    
      AudioData,
    
    } from "sarvam-conv-ai-sdk/react-native";
    
    class MyRNAudioInterface implements AsyncAudioInterface {
    
      async start(
    
        inputCallback: (audioData: AudioData, frameCount: number) => Promise<void>,
    
      ): Promise<void> {
    
        // Initialize your audio recording library
    
        // Call inputCallback with a Uint8Array of 16-bit PCM data
    
      }
    
      async output(audio: Uint8Array, sampleRate?: number): Promise<void> {
    
        // Play 16-bit PCM mono through the speaker
    
      }
    
      interrupt(): void {
    
        // Stop all queued and playing audio (user barge-in)
    
      }
    
      async stop(): Promise<void> {
    
        // Release microphone and audio resources
    
      }
    
    }

Recommended libraries:

  * [react-native-audio-api](https://github.com/software-mansion/react-native-audio-api) — low-level audio API
  * [expo-av](https://docs.expo.dev/versions/latest/sdk/av/) — Expo projects
  * [react-native-live-audio-stream](https://github.com/niceDev0908/react-native-live-audio-stream) — real-time streaming



## Session methods

Method| Description  
---|---  
`await agent.start()`| Fetch a signed WebSocket URL and connect  
`await agent.waitForConnect(timeout?)`| Wait until connected; `timeout` is in seconds (returns `false` on timeout)  
`await agent.sendAudio(data)`| Send a raw PCM audio chunk  
`agent.isConnected()`| Current connection status  
`agent.getInteractionId()`| The current interaction (call) ID, once connected  
`agent.getState()`| Current `AgentState`  
`agent.mute()` / `agent.unmute()`| Mute or unmute the microphone without disconnecting. While muted, the SDK sends silence so VAD stays stable  
`agent.isMuted()`| Current mute status  
`await agent.waitForDisconnect()`| Wait until the session ends  
`await agent.stop()`| Close the connection and clean up  
  
Call `await agent.stop()` on unmount so the WebSocket and audio interface are cleaned up. Reconnection is not supported: each WebSocket URL is single-use. If the connection drops, call `stop()` and create a new `ConversationAgent`.

Stop or recreate the agent when the app backgrounds. React Native suspends WebSockets in the background, and you cannot reuse the old URL:
    
    
    import { useEffect, useRef } from "react";
    
    import { AppState, AppStateStatus } from "react-native";
    
    const appState = useRef(AppState.currentState);
    
    useEffect(() => {
    
      const subscription = AppState.addEventListener(
    
        "change",
    
        (nextState: AppStateStatus) => {
    
          if (appState.current.match(/active/) && nextState === "background") {
    
            agentRef.current?.stop();
    
          }
    
          appState.current = nextState;
    
        },
    
      );
    
      return () => {
    
        subscription.remove();
    
        agentRef.current?.stop().catch(console.error);
    
      };
    
    }, []);

## Troubleshooting

**Microphone permission denied.** Request the microphone before starting a voice session.

Expo:
    
    
    import { Audio } from "expo-av";
    
    const { granted } = await Audio.requestPermissionsAsync();
    
    if (!granted) {
    
      // Ask the user to enable the permission in Settings
    
    }

Bare React Native, with [react-native-permissions](https://github.com/zoontek/react-native-permissions):
    
    
    import { request, PERMISSIONS, RESULTS } from "react-native-permissions";
    
    import { Platform } from "react-native";
    
    const result = await request(
    
      Platform.OS === "ios"
    
        ? PERMISSIONS.IOS.MICROPHONE
    
        : PERMISSIONS.ANDROID.RECORD_AUDIO,
    
    );
    
    if (result !== RESULTS.GRANTED) {
    
      // Handle denied permission
    
    }

**No audio output.** Check device volume and the iOS silent switch. Confirm `output()` writes to the speaker at `output_sample_rate`.

**Connection timeout.** Check connectivity, API key, `org_id` / `workspace_id` / `app_id`, and that the agent has a committed version.

Never embed your API key in the app binary. Point `baseUrl` at a backend you control, leave `apiKey` empty, and pass your app auth in `customHeaders` (cookies are not available in React Native):
    
    
    const agent = new ConversationAgent({
    
      apiKey: "",
    
      baseUrl: "https://api.yourapp.com/sarvam/",
    
      customHeaders: {
    
        Authorization: "Bearer eyJhbGciOiJIUzI1NiIs...",
    
        "X-User-Id": "user-123",
    
      },
    
      platform: "react-native",
    
      audioInterface: new MyRNAudioInterface(),
    
      config: {
    
        // ...
    
      },
    
    });

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/deploy/sdks/web)[FlutterNext](https://docs.sarvam.ai/voice-agents/deploy/sdks/flutter)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Introduction](https://docs.sarvam.ai/voice-agents/introduction)
    * [Why Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents)
    * [Overview](https://docs.sarvam.ai/voice-agents/overview)
    * [Quickstart](https://docs.sarvam.ai/voice-agents/quickstart)
    * [MCP Server](https://docs.sarvam.ai/voice-agents/mcp)
  * Build

    * [Overview](https://docs.sarvam.ai/voice-agents/build/overview)
    * Architecture

    * [Navigating the build interface](https://docs.sarvam.ai/voice-agents/build/navigating-workspace)
    * [Agent](https://docs.sarvam.ai/voice-agents/build/agent/overview)

    * [Prompt Practices](https://docs.sarvam.ai/voice-agents/build/single-state-agents)
    * [Building & improving agents](https://docs.sarvam.ai/voice-agents/build/process)
    * [Genie](https://docs.sarvam.ai/voice-agents/build/genie)
    * [Tests](https://docs.sarvam.ai/voice-agents/build/tests)

    * Advanced concepts

  * Deploy

    * [Overview](https://docs.sarvam.ai/voice-agents/deploy/overview)
    * [Phone Numbers](https://docs.sarvam.ai/voice-agents/deploy/telephony)

    * [Inbounds](https://docs.sarvam.ai/voice-agents/deploy/inbounds)
    * [Campaigns](https://docs.sarvam.ai/voice-agents/deploy/campaigns)

    * [Deploy with Code (API & SDK)](https://docs.sarvam.ai/voice-agents/deploy/deploy-with-code)
  * Monitor

    * [Overview](https://docs.sarvam.ai/voice-agents/monitor/overview)
    * [Agent Analytics](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics)

    * [Boards](https://docs.sarvam.ai/voice-agents/monitor/boards)

    * [SQL best practices](https://docs.sarvam.ai/voice-agents/monitor/clickhouse-sql-best-practices)
  * SDKs

    * [Python](https://docs.sarvam.ai/voice-agents/deploy/sdks/python)
    * [Web (TypeScript)](https://docs.sarvam.ai/voice-agents/deploy/sdks/web)
    * [React Native](https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native)
    * [Flutter](https://docs.sarvam.ai/voice-agents/deploy/sdks/flutter)
  * API Reference

    * [Introduction](https://docs.sarvam.ai/voice-agents/api/introduction)
    * Deployments

    * Campaigns

    * Instant Outbound

    * Analytics

    * Boards

    * Tests

    * BYOK

  * Settings

    * [API Key](https://docs.sarvam.ai/voice-agents/settings/api-key)
    * [Secrets](https://docs.sarvam.ai/voice-agents/settings/secrets)
    * [Policy](https://docs.sarvam.ai/voice-agents/settings/policy)
    * [Data retention](https://docs.sarvam.ai/api/platform/data-retention "Data retention")
    * [Extensions](https://docs.sarvam.ai/voice-agents/settings/extensions)
    * [Pricing](https://docs.sarvam.ai/voice-agents/pricing)



  * [Introduction](https://docs.sarvam.ai/voice-agents/introduction)
  * [Why Voice Agents](https://docs.sarvam.ai/voice-agents/why-voice-agents)
  * [Overview](https://docs.sarvam.ai/voice-agents/overview)
  * [Quickstart](https://docs.sarvam.ai/voice-agents/quickstart)
  * [MCP Server](https://docs.sarvam.ai/voice-agents/mcp)
  * [Overview](https://docs.sarvam.ai/voice-agents/build/overview)
  * [Introduction](https://docs.sarvam.ai/voice-agents/build/concepts/introduction)
  * [Run-time](https://docs.sarvam.ai/voice-agents/build/run-time)
  * [Models](https://docs.sarvam.ai/voice-agents/build/models)
  * [Harness](https://docs.sarvam.ai/voice-agents/build/concepts/harness)
  * [Navigating the build interface](https://docs.sarvam.ai/voice-agents/build/navigating-workspace)
  * [Agent](https://docs.sarvam.ai/voice-agents/build/agent/overview)
  * [Instruction](https://docs.sarvam.ai/voice-agents/build/system-prompt)
  * [Variables & personalization](https://docs.sarvam.ai/voice-agents/build/variables-personalization)
  * [Tools](https://docs.sarvam.ai/voice-agents/build/tools)
  * [Core tools](https://docs.sarvam.ai/voice-agents/build/tools/core-tools)
  * [Call transfer](https://docs.sarvam.ai/voice-agents/build/tools/call-transfer)
  * [API tool](https://docs.sarvam.ai/voice-agents/build/tools/https-tool)
  * [Data validation & verification](https://docs.sarvam.ai/voice-agents/build/tools/data-validation)
  * [Mocking a tool](https://docs.sarvam.ai/voice-agents/build/tools/mocking-a-tool)
  * [Code Tools](https://docs.sarvam.ai/voice-agents/build/tools/code-tools)
  * [On-start & on-end hooks](https://docs.sarvam.ai/voice-agents/build/on-start-on-end-hooks)
  * [Knowledge base](https://docs.sarvam.ai/voice-agents/build/knowledge-base)
  * [Agent versioning](https://docs.sarvam.ai/voice-agents/build/agent/versioning)
  * [Speakers & voice](https://docs.sarvam.ai/voice-agents/build/voice-language)
  * [Conversation settings](https://docs.sarvam.ai/voice-agents/build/conversation-settings)
  * [Prompt Practices](https://docs.sarvam.ai/voice-agents/build/single-state-agents)
  * [Building & improving agents](https://docs.sarvam.ai/voice-agents/build/process)
  * [Genie](https://docs.sarvam.ai/voice-agents/build/genie)
  * [Tests](https://docs.sarvam.ai/voice-agents/build/tests)
  * [Write test cases](https://docs.sarvam.ai/voice-agents/build/tests/write-test-cases)
  * [Run tests & review results](https://docs.sarvam.ai/voice-agents/build/tests/run-tests)
  * [Multi-state agents](https://docs.sarvam.ai/voice-agents/build/states-conversation-flow)
  * [Overview](https://docs.sarvam.ai/voice-agents/deploy/overview)
  * [Phone Numbers](https://docs.sarvam.ai/voice-agents/deploy/telephony)
  * [Bring Your Own Telephony](https://docs.sarvam.ai/voice-agents/deploy/telephony/bring-your-own)
  * [Exotel](https://docs.sarvam.ai/voice-agents/deploy/telephony/exotel)
  * [Twilio](https://docs.sarvam.ai/voice-agents/deploy/telephony/twilio)
  * [Smartflo](https://docs.sarvam.ai/voice-agents/deploy/telephony/smartflo)
  * [Pulse](https://docs.sarvam.ai/voice-agents/deploy/telephony/pulse)
  * [Intalk](https://docs.sarvam.ai/voice-agents/deploy/telephony/intalk)
  * [Vobiz](https://docs.sarvam.ai/voice-agents/deploy/telephony/vobiz)
  * [Plivo](https://docs.sarvam.ai/voice-agents/deploy/telephony/plivo)
  * [Rent from Sarvam](https://docs.sarvam.ai/voice-agents/deploy/telephony/rent-from-sarvam)
  * [Manage Phone Numbers](https://docs.sarvam.ai/voice-agents/deploy/telephony/manage-numbers)
  * [Groups](https://docs.sarvam.ai/voice-agents/deploy/telephony/groups)
  * [Inbounds](https://docs.sarvam.ai/voice-agents/deploy/inbounds)
  * [Campaigns](https://docs.sarvam.ai/voice-agents/deploy/campaigns)
  * [Create a campaign](https://docs.sarvam.ai/voice-agents/deploy/campaigns/create-campaign)
  * [Campaign details](https://docs.sarvam.ai/voice-agents/deploy/campaigns/campaign-details)
  * [Cohorts](https://docs.sarvam.ai/voice-agents/deploy/campaigns/cohorts)
  * [Dialing rate & concurrency](https://docs.sarvam.ai/voice-agents/deploy/campaigns/dialing-rate)
  * [Campaign lifecycle](https://docs.sarvam.ai/voice-agents/deploy/campaigns/campaign-lifecycle)
  * [Do Not Disturb (DND)](https://docs.sarvam.ai/voice-agents/deploy/campaigns/dnd)
  * [Best practices](https://docs.sarvam.ai/voice-agents/deploy/campaigns/best-practices)
  * [Deploy with Code (API & SDK)](https://docs.sarvam.ai/voice-agents/deploy/deploy-with-code)
  * [Overview](https://docs.sarvam.ai/voice-agents/monitor/overview)
  * [Agent Analytics](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics)
  * [Overview tab](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/overview)
  * [Connectivity](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/connectivity)
  * [Engagement](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/engagement)
  * [Tools](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/tools)
  * [Goals](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/goals)
  * [Group by](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/group-by)
  * [Call Logs](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/call-logs)
  * [Log Analyser](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/log-analyser)
  * [Boards](https://docs.sarvam.ai/voice-agents/monitor/boards)
  * [Create a board](https://docs.sarvam.ai/voice-agents/monitor/boards/create-board)
  * [Create a widget](https://docs.sarvam.ai/voice-agents/monitor/boards/create-widget)
  * [Filters](https://docs.sarvam.ai/voice-agents/monitor/boards/filters)
  * [SQL best practices](https://docs.sarvam.ai/voice-agents/monitor/clickhouse-sql-best-practices)
  * [Python](https://docs.sarvam.ai/voice-agents/deploy/sdks/python)
  * [Web (TypeScript)](https://docs.sarvam.ai/voice-agents/deploy/sdks/web)
  * [React Native](https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native)
  * [Flutter](https://docs.sarvam.ai/voice-agents/deploy/sdks/flutter)
  * [Introduction](https://docs.sarvam.ai/voice-agents/api/introduction)
  * [Create deployment](https://docs.sarvam.ai/voice-agents/api/deployments/create)
  * [List deployments](https://docs.sarvam.ai/voice-agents/api/deployments/list)
  * [Get deployment](https://docs.sarvam.ai/voice-agents/api/deployments/get)
  * [Update deployment](https://docs.sarvam.ai/voice-agents/api/deployments/update)
  * [Update status](https://docs.sarvam.ai/voice-agents/api/deployments/update-status)
  * [Delete deployment](https://docs.sarvam.ai/voice-agents/api/deployments/delete)
  * [Webhook payload](https://docs.sarvam.ai/voice-agents/api/deployments/webhooks/webhook-payload)
  * [List webhook deliveries](https://docs.sarvam.ai/voice-agents/api/deployments/webhooks/list)
  * [Retry webhook deliveries](https://docs.sarvam.ai/voice-agents/api/deployments/webhooks/retry)
  * [Upload cohort](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/upload)
  * [Stream cohort](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/stream)
  * [List cohorts](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/list)
  * [Get cohort](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/get)
  * [Download cohort file](https://docs.sarvam.ai/voice-agents/api/deployments/cohorts/download)
  * [Create campaign](https://docs.sarvam.ai/voice-agents/api/campaigns/create)
  * [List campaigns](https://docs.sarvam.ai/voice-agents/api/campaigns/list)
  * [Get campaign](https://docs.sarvam.ai/voice-agents/api/campaigns/get)
  * [Update campaign](https://docs.sarvam.ai/voice-agents/api/campaigns/update)
  * [Update status](https://docs.sarvam.ai/voice-agents/api/campaigns/update-status)
  * [Webhook payload](https://docs.sarvam.ai/voice-agents/api/campaigns/webhooks/webhook-payload)
  * [List webhook deliveries](https://docs.sarvam.ai/voice-agents/api/campaigns/webhooks/list)
  * [Retry webhook deliveries](https://docs.sarvam.ai/voice-agents/api/campaigns/webhooks/retry)
  * [Upload cohort](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/upload)
  * [Stream cohort](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/stream)
  * [List cohorts](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/list)
  * [Get cohort](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/get)
  * [Download cohort file](https://docs.sarvam.ai/voice-agents/api/campaigns/cohorts/download)
  * [Create outbound call](https://docs.sarvam.ai/voice-agents/api/instant-outbound/create)
  * [Webhook payload](https://docs.sarvam.ai/voice-agents/api/instant-outbound/webhook-payload)
  * [Overview](https://docs.sarvam.ai/voice-agents/api/analytics/overview)
  * [List attempts](https://docs.sarvam.ai/voice-agents/api/analytics/attempts)
  * [List interactions](https://docs.sarvam.ai/voice-agents/api/analytics/interactions)
  * [Get recording](https://docs.sarvam.ai/voice-agents/api/analytics/recordings)
  * [Get transcript](https://docs.sarvam.ai/voice-agents/api/analytics/transcripts)
  * [Overview](https://docs.sarvam.ai/voice-agents/api/boards/overview)
  * [Writing board SQL](https://docs.sarvam.ai/voice-agents/api/boards/sql)
  * [Best practices](https://docs.sarvam.ai/voice-agents/api/boards/best-practices)
  * [List boards](https://docs.sarvam.ai/voice-agents/api/boards/list)
  * [Create board](https://docs.sarvam.ai/voice-agents/api/boards/create)
  * [Get board](https://docs.sarvam.ai/voice-agents/api/boards/get)
  * [Update board](https://docs.sarvam.ai/voice-agents/api/boards/update)
  * [Duplicate board](https://docs.sarvam.ai/voice-agents/api/boards/duplicate)
  * [Create tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/create)
  * [Update tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/update)
  * [Run tab](https://docs.sarvam.ai/voice-agents/api/boards/tabs/run)
  * [Create widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/create)
  * [Update widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/update)
  * [Duplicate widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/duplicate)
  * [Run widget](https://docs.sarvam.ai/voice-agents/api/boards/widgets/run)
  * [List filters](https://docs.sarvam.ai/voice-agents/api/boards/filters/list)
  * [Update filter](https://docs.sarvam.ai/voice-agents/api/boards/filters/update)
  * [Create notification rule](https://docs.sarvam.ai/voice-agents/api/boards/notifications/create)
  * [List notification rules](https://docs.sarvam.ai/voice-agents/api/boards/notifications/list)
  * [Get notification rule](https://docs.sarvam.ai/voice-agents/api/boards/notifications/get)
  * [Update notification rule](https://docs.sarvam.ai/voice-agents/api/boards/notifications/update)
  * [Get query schema](https://docs.sarvam.ai/voice-agents/api/boards/query/schema)
  * [Preview query](https://docs.sarvam.ai/voice-agents/api/boards/query/preview)
  * [Overview](https://docs.sarvam.ai/voice-agents/api/tests/overview)
  * [Best practices](https://docs.sarvam.ai/voice-agents/api/tests/best-practices)
  * [List test suites](https://docs.sarvam.ai/voice-agents/api/tests/list)
  * [Create a test suite](https://docs.sarvam.ai/voice-agents/api/tests/create)
  * [Get a test suite](https://docs.sarvam.ai/voice-agents/api/tests/get)
  * [Update a test suite](https://docs.sarvam.ai/voice-agents/api/tests/update)
  * [Add a test case](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/add)
  * [Get a test case](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/get)
  * [Update a test case](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/update)
  * [Duplicate a test case](https://docs.sarvam.ai/voice-agents/api/tests/test-cases/duplicate)
  * [Map suite variables onto an app](https://docs.sarvam.ai/voice-agents/api/tests/mappings/create)
  * [Get the variable mapping](https://docs.sarvam.ai/voice-agents/api/tests/mappings/get)
  * [Run a test suite](https://docs.sarvam.ai/voice-agents/api/tests/runs/run-suite)
  * [Run a single test case](https://docs.sarvam.ai/voice-agents/api/tests/runs/run-test-case)
  * [List runs](https://docs.sarvam.ai/voice-agents/api/tests/runs/list)
  * [Get a run](https://docs.sarvam.ai/voice-agents/api/tests/runs/get)
  * [Get test case results](https://docs.sarvam.ai/voice-agents/api/tests/runs/results)
  * [Overview](https://docs.sarvam.ai/voice-agents/api/byok/overview)
  * [Obtain access token](https://docs.sarvam.ai/voice-agents/api/byok/auth)
  * [Decrypt key](https://docs.sarvam.ai/voice-agents/api/byok/decrypt-key)
  * [Rotate key](https://docs.sarvam.ai/voice-agents/api/byok/rotate-key)
  * [API Key](https://docs.sarvam.ai/voice-agents/settings/api-key)
  * [Secrets](https://docs.sarvam.ai/voice-agents/settings/secrets)
  * [Policy](https://docs.sarvam.ai/voice-agents/settings/policy)
  * [Extensions](https://docs.sarvam.ai/voice-agents/settings/extensions)
  * [Pricing](https://docs.sarvam.ai/voice-agents/pricing)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)



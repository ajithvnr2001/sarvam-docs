---
url: https://docs.sarvam.ai/voice-agents/deploy/sdks/flutter/
title: Flutter | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:27.533410+00:00
---

# Flutter | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/deploy/sdks/flutter/

Skip to navigation

On this page

  * Install
  * Start a voice session
  * InteractionConfig
  * Callbacks
  * DefaultAudioInterface
  * Session methods
  * Troubleshooting



Scroll to top

[SDKs](https://docs.sarvam.ai/voice-agents/deploy/sdks/python)

# Flutter

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/deploy/sdks/flutter.md "View this page as plain text")|More actions

This page is for Voice Agents.

For real-time voice on iOS and Android, the Flutter SDK (`sarvamconv_ai_sdk`) wraps the [WebSocket interface](https://docs.sarvam.ai/voice-agents/deploy/deploy-with-code#websocket-integration) in `SamvaadAgent`, with `DefaultAudioInterface` for microphone capture and playback.

## Install

Add the SDK to `pubspec.yaml`:
    
    
    dependencies:
    
      sarvamconv_ai_sdk: ^1.0.0
    
    
    flutter pub get

**iOS.** Add microphone permission to `ios/Runner/Info.plist`:
    
    
    <key>NSMicrophoneUsageDescription</key>
    
    <string>This app needs microphone access for voice conversations</string>

**Android.** Add permissions to `android/app/src/main/AndroidManifest.xml`:
    
    
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    
    <uses-permission android:name="android.permission.INTERNET" />

## Start a voice session
    
    
    import 'package:flutter/material.dart';
    
    import 'package:sarvamconv_ai_sdk/sarvamconv_ai_sdk.dart';
    
    class VoiceChat extends StatefulWidget {
    
      const VoiceChat({super.key});
    
      @override
    
      State<VoiceChat> createState() => _VoiceChatState();
    
    }
    
    class _VoiceChatState extends State<VoiceChat> {
    
      SamvaadAgent? _agent;
    
      DefaultAudioInterface? _audioInterface;
    
      bool _isConnected = false;
    
      String _transcript = '';
    
      Future<void> startConversation() async {
    
        _audioInterface = DefaultAudioInterface(inputSampleRate: 16000);
    
        final config = InteractionConfig(
    
          orgId: 'your_org_id',
    
          workspaceId: 'your_workspace_id',
    
          appId: 'your_app_id',
    
          userIdentifier: 'user123',
    
          userIdentifierType: UserIdentifierType.custom,
    
          interactionType: InteractionType.call,
    
          sampleRate: 16000,
    
        );
    
        _agent = SamvaadAgent(
    
          apiKey: 'your_api_key',
    
          config: config,
    
          audioInterface: _audioInterface,
    
          textCallback: (msg) async {
    
            if (msg is ServerTextChunkMsg) {
    
              setState(() => _transcript += msg.text);
    
            }
    
          },
    
          eventCallback: (event) async {
    
            if (event is ServerInteractionConnectedEvent) {
    
              setState(() => _isConnected = true);
    
            } else if (event is ServerInteractionEndEvent) {
    
              setState(() => _isConnected = false);
    
            }
    
          },
    
        );
    
        await _agent!.start();
    
        final connected = await _agent!.waitForConnect(
    
          timeout: const Duration(seconds: 10),
    
        );
    
        if (!connected) {
    
          throw Exception('Connection timeout');
    
        }
    
      }
    
      Future<void> stopConversation() async {
    
        await _agent?.stop();
    
        _agent = null;
    
        _audioInterface = null;
    
        setState(() => _isConnected = false);
    
      }
    
      @override
    
      void dispose() {
    
        stopConversation();
    
        super.dispose();
    
      }
    
      @override
    
      Widget build(BuildContext context) {
    
        return Scaffold(
    
          appBar: AppBar(title: const Text('Voice Chat')),
    
          body: Column(
    
            children: [
    
              ElevatedButton(
    
                onPressed: _isConnected ? stopConversation : startConversation,
    
                child: Text(_isConnected ? 'Stop Voice Chat' : 'Start Voice Chat'),
    
              ),
    
              Expanded(
    
                child: SingleChildScrollView(
    
                  child: Text('Transcript: $_transcript'),
    
                ),
    
              ),
    
            ],
    
          ),
    
        );
    
      }
    
    }

`DefaultAudioInterface` captures the microphone and plays agent audio (16-bit PCM mono at 8 kHz, 16 kHz, or 48 kHz). `start()` fetches a signed WebSocket URL and begins streaming.

## InteractionConfig

Field| Required| Description  
---|---|---  
`userIdentifierType`| Yes| `UserIdentifierType.custom`, `.email`, `.phoneNumber`, or `.unknown`  
`userIdentifier`| Yes| The identifier value; also what you search by in [Log Analyser](https://docs.sarvam.ai/voice-agents/monitor/agent-analytics/log-analyser)  
`orgId`| Yes| Your organization ID  
`workspaceId`| Yes| Your workspace ID  
`appId`| Yes| The agent to connect to  
`interactionType`| Yes| `InteractionType.call` for a voice session  
`sampleRate`| Yes| `8000`, `16000`, or `48000` (16-bit PCM mono)  
`version`| No| Pins a specific committed agent version. If omitted, the SDK uses the latest committed version, and the connection fails if the agent has no committed version  
`agentVariables`| No| Seed [agent variables](https://docs.sarvam.ai/voice-agents/build/variables-personalization) at session start  
`initialLanguageName`| No| Starting language; must be one of the agent’s allowed languages (for example `SarvamToolLanguageName.hindi`)  
`initialStateName`| No| Starting state, if the agent uses [states](https://docs.sarvam.ai/voice-agents/build/states-conversation-flow)  
`initialBotMessage`| No| First message from the agent  
  
## Callbacks

Pass any of these to `SamvaadAgent` to react to what happens during the call:

Callback| Fires with| Use it for  
---|---|---  
`textCallback`| `ServerTextMsg` or `ServerTextChunkMsg`| Streaming or complete agent text  
`audioCallback`| audio chunk (`audioBytes`, `sampleRate`)| Raw agent audio, if you’re handling playback yourself instead of using `audioInterface`  
`eventCallback`| session event| `ServerInteractionConnectedEvent`, `ServerUserInterruptEvent`, `ServerInteractionEndEvent`, speech start/end, language change, state transition, variable update  
  
## DefaultAudioInterface
    
    
    final audioInterface = DefaultAudioInterface(
    
      inputSampleRate: 16000,
    
      outputSampleRate: 16000,
    
    );

To bring your own I/O, implement `AudioInterface`:
    
    
    class CustomAudioInterface implements AudioInterface {
    
      @override
    
      Future<void> start(AudioInputCallback inputCallback) async {
    
        // Capture audio and call inputCallback with chunks
    
      }
    
      @override
    
      Future<void> output(Uint8List audio, {int? sampleRate}) async {
    
        // Play audio through the speaker
    
      }
    
      @override
    
      void interrupt() {
    
        // Stop queued playback
    
      }
    
      @override
    
      Future<void> stop() async {
    
        // Cleanup
    
      }
    
    }

## Session methods

Method| Description  
---|---  
`await agent.start()`| Fetch a signed WebSocket URL and connect  
`await agent.waitForConnect(timeout: Duration(seconds: 10))`| Wait until connected (returns `false` on timeout)  
`await agent.sendAudio(audioBytes)`| Send raw 16-bit PCM mono at `config.sampleRate`  
`agent.isConnected`| Current connection status  
`agent.interactionId`| The current interaction (call) ID, once connected  
`await agent.waitForDisconnect()`| Wait until the session ends  
`await agent.stop()`| Close the connection and clean up  
  
Call `await agent.stop()` in `dispose()` so the WebSocket and audio interface are cleaned up. Reconnection is not supported: each WebSocket URL is single-use. If the connection drops, call `stop()` and create a new `SamvaadAgent`.

Stop the agent when the app goes to the background:
    
    
    class _MyWidgetState extends State<MyWidget> with WidgetsBindingObserver {
    
      @override
    
      void initState() {
    
        super.initState();
    
        WidgetsBinding.instance.addObserver(this);
    
      }
    
      @override
    
      void dispose() {
    
        WidgetsBinding.instance.removeObserver(this);
    
        _agent?.stop();
    
        super.dispose();
    
      }
    
      @override
    
      void didChangeAppLifecycleState(AppLifecycleState state) {
    
        if (state == AppLifecycleState.paused) {
    
          _agent?.stop();
    
        }
    
      }
    
    }

## Troubleshooting

**Microphone permission denied.** Request the microphone before starting:
    
    
    import 'package:permission_handler/permission_handler.dart';
    
    final status = await Permission.microphone.request();
    
    if (!status.isGranted) {
    
      // Ask the user to enable the permission
    
    }

**No audio output.** Check device volume, that `DefaultAudioInterface` is initialized, and that `sampleRate` matches the session config.

**Connection timeout.** Check connectivity, API key, `orgId` / `workspaceId` / `appId`, and that the agent has a committed version.

Never embed your API key in the app binary. Omit `apiKey`, set `baseUrl` to a backend you control, and pass your app auth in `headers`:
    
    
    final agent = SamvaadAgent(
    
      config: config,
    
      baseUrl: 'https://your-proxy-server.com/sarvam-proxy/',
    
      headers: {
    
        'Authorization': 'Bearer user_session_token',
    
      },
    
      audioInterface: DefaultAudioInterface(inputSampleRate: 16000),
    
    );

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native)[IntroductionManage deployments, campaigns, outbound calls, and analytics for your voice agents over REST.Next](https://docs.sarvam.ai/voice-agents/api/introduction)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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



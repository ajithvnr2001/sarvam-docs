---
url: https://docs.sarvam.ai/voice-agents/deploy/sdks/web/
title: Web (TypeScript) | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:28.243874+00:00
---

# Web (TypeScript) | Sarvam API Docs

> Source: https://docs.sarvam.ai/voice-agents/deploy/sdks/web/

Skip to navigation

On this page

  * Install
  * Start a voice session
  * InteractionConfig
  * Callbacks
  * BrowserAudioInterface
  * Session methods
  * React example
  * Troubleshooting



Scroll to top

[SDKs](https://docs.sarvam.ai/voice-agents/deploy/sdks/python)

# Web (TypeScript)

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/voice-agents/deploy/sdks/web.md "View this page as plain text")|More actions

This page is for Voice Agents.

For real-time voice in the browser, the TypeScript SDK (`sarvam-conv-ai-sdk/browser`) wraps the [WebSocket interface](https://docs.sarvam.ai/voice-agents/deploy/deploy-with-code#websocket-integration) in a typed client, `ConversationAgent`, with `BrowserAudioInterface` for microphone capture and playback.

## Install
    
    
    npm install sarvam-conv-ai-sdk

Use the `/browser` entry point for a smaller bundle:
    
    
    import {
    
      ConversationAgent,
    
      BrowserAudioInterface,
    
    } from "sarvam-conv-ai-sdk/browser";

## Start a voice session
    
    
    import {
    
      ConversationAgent,
    
      BrowserAudioInterface,
    
      InteractionType,
    
    } from "sarvam-conv-ai-sdk/browser";
    
    const audioInterface = new BrowserAudioInterface();
    
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
    
      transcriptCallback: async (msg) => {
    
        console.log(`${msg.role}: ${msg.content}`);
    
      },
    
    });
    
    await agent.start();
    
    await agent.waitForConnect(10);

`BrowserAudioInterface` captures the microphone and plays agent audio (16-bit PCM mono). `agent.start()` fetches a signed WebSocket URL, sends the session start message, and begins streaming. Call `start()` from a user gesture (for example a button click) so the browser allows audio playback.

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
  
## BrowserAudioInterface
    
    
    new BrowserAudioInterface(
    
      sampleRate?: number,  // Default: 16000
    
      options?: {
    
        prebufferMs?: number;      // Default: 700
    
        bufferSizeMs?: number;     // Default: 8000
    
        outputLevelCallback?: (level: { rms: number; peak: number; db: number }) => void;
    
      }
    
    )

`BrowserAudioInterface` uses adaptive buffering to handle network jitter. Adjust `prebufferMs` for your network:

Network condition| `prebufferMs`| Notes  
---|---|---  
Good/stable| `300`–`500`| Lower latency; may gap on jitter  
Normal| `700` (default)| Balanced latency and stability  
Unstable| `1000`–`1500`| Higher latency, smoother playback  
  
Use `audioLevelCallback` on the agent (or `outputLevelCallback` on the interface) to drive a speaking indicator:
    
    
    const agent = new ConversationAgent({
    
      // ...config
    
      audioLevelCallback: (level) => {
    
        updateAgentSpeakingIndicator(level);
    
      },
    
    });

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
  
Call `await agent.stop()` on unmount (or in a `finally` block) so the WebSocket and audio interface are cleaned up even if the session errors out. Reconnection is not supported: each WebSocket URL is single-use. If the connection drops, call `stop()` and create a new `ConversationAgent`.

## React example
    
    
    import React, { useRef, useState, useEffect } from "react";
    
    import {
    
      ConversationAgent,
    
      BrowserAudioInterface,
    
      InteractionType,
    
      AgentState,
    
      Role,
    
    } from "sarvam-conv-ai-sdk/browser";
    
    interface Message {
    
      role: "user" | "bot";
    
      content: string;
    
    }
    
    function VoiceChat() {
    
      const [state, setState] = useState<AgentState>(AgentState.IDLE);
    
      const [messages, setMessages] = useState<Message[]>([]);
    
      const [isMuted, setIsMuted] = useState(false);
    
      const agentRef = useRef<ConversationAgent | null>(null);
    
      useEffect(() => {
    
        return () => {
    
          agentRef.current?.stop().catch(console.error);
    
        };
    
      }, []);
    
      const startConversation = async () => {
    
        const audioInterface = new BrowserAudioInterface(16000, {
    
          outputLevelCallback: (level) => {
    
            // Update volume visualization
    
          },
    
        });
    
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
    
          stateCallback: (newState) => setState(newState),
    
          transcriptCallback: async (msg) => {
    
            setMessages((prev) => [
    
              ...prev,
    
              { role: msg.role === Role.USER ? "user" : "bot", content: msg.content },
    
            ]);
    
          },
    
          endCallback: async () => {
    
            agentRef.current = null;
    
            setState(AgentState.IDLE);
    
          },
    
        });
    
        agentRef.current = agent;
    
        await agent.start();
    
      };
    
      const toggleMute = () => {
    
        if (!agentRef.current) return;
    
        if (agentRef.current.isMuted()) {
    
          agentRef.current.unmute();
    
          setIsMuted(false);
    
        } else {
    
          agentRef.current.mute();
    
          setIsMuted(true);
    
        }
    
      };
    
      return (
    
        <div>
    
          <p>State: {state}</p>
    
          <button onClick={startConversation} disabled={state !== AgentState.IDLE}>
    
            Start
    
          </button>
    
          <button onClick={() => agentRef.current?.stop()} disabled={state === AgentState.IDLE}>
    
            Stop
    
          </button>
    
          <button onClick={toggleMute} disabled={state === AgentState.IDLE}>
    
            {isMuted ? "Unmute" : "Mute"}
    
          </button>
    
          <div>
    
            {messages.map((msg, i) => (
    
              <p key={i}>
    
                <strong>{msg.role === "user" ? "You" : "Agent"}:</strong> {msg.content}
    
              </p>
    
            ))}
    
          </div>
    
        </div>
    
      );
    
    }
    
    export default VoiceChat;

## Troubleshooting

**`audioInterface` is required for CALL interactions.** Pass a `BrowserAudioInterface`:
    
    
    const agent = new ConversationAgent({
    
      audioInterface: new BrowserAudioInterface(),
    
      // ...
    
    });

**Audio doesn’t play in Firefox.** Firefox requires a user gesture before playing audio. Call `start()` from a click handler.

**HTTPS is required for the microphone** in production. `localhost` is enough for development.

**Microphone permission errors:**
    
    
    try {
    
      const audioInterface = new BrowserAudioInterface();
    
      const agent = new ConversationAgent({
    
        audioInterface,
    
        // ...
    
      });
    
      await agent.start();
    
    } catch (err) {
    
      if (err.name === "NotAllowedError") {
    
        console.error("Microphone permission denied");
    
      } else if (err.name === "NotFoundError") {
    
        console.error("No microphone found");
    
      } else if (err.name === "NotReadableError") {
    
        console.error("Microphone is in use");
    
      }
    
    }

Never embed your API key in client-side code. Point `baseUrl` at a backend you control and leave `apiKey` empty so the proxy adds the Sarvam key server-side.
    
    
    const agent = new ConversationAgent({
    
      apiKey: "",
    
      baseUrl: "/api/sarvam/",
    
      config: {
    
        // ...
    
      },
    
      audioInterface: new BrowserAudioInterface(),
    
    });

For a cross-origin proxy, pass your app’s auth in `customHeaders` (for example `Authorization: Bearer` plus your session token).

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/voice-agents/deploy/sdks/python)[React NativeNext](https://docs.sarvam.ai/voice-agents/deploy/sdks/react-native)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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



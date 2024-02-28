using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Oculus.Interaction;
using System;
using M2MqttUnity.Examples;

public class ButtonLogic : MonoBehaviour
{
    public String PayloadVar;
    public M2MqttUnityTest client;
    public bool isConnectButton;
    public bool isPistonButton;
    public bool isBeltButton;
    public MachineModelBehaviour machineModelBehaviour;

    public bool testIsRunning = false;
    public float testStartedAt;
    
    

    public event Action<PointerEvent> WhenPointerEventRaised;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (GetComponent<PokeInteractable>().State == InteractableState.Select)
        {
            if (isConnectButton)
            {
                client.SetBrokerAddress("10.52.249.73");
                client.SetBrokerPort("1883");
                client.Connect();
            }
            else if(isPistonButton)
            {
                if(PayloadVar == "true")
                {
                    machineModelBehaviour.extendPiston = true;
                }
                else
                {
                    machineModelBehaviour.extendPiston = false;
                }
                client.PublishPayload(PayloadVar);
            }
            else if(isBeltButton)
            {
                testIsRunning = true;
                testStartedAt = Time.time;
            }

            //client.TestPublish();
            //this.gameObject.SetActive(false);
        }
        if (testIsRunning)
        {
            if (Time.time - testStartedAt > 2)
            {
                machineModelBehaviour.highlightBelt = true;
                testIsRunning = false;
            }
        }

    }

}

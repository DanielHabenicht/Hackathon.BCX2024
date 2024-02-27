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
            else
            {
                client.PublishPayload(PayloadVar);
            }

            //client.TestPublish();
            //this.gameObject.SetActive(false);
        }
   
    }

}

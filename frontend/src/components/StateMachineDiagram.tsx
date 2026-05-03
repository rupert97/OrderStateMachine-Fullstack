import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
    startOnLoad: true,
    theme: 'base',
    themeVariables: {
        primaryColor: '#f3f4f6',
        primaryTextColor: '#1f2937',
        primaryBorderColor: '#d1d5db',
        lineColor: '#9ca3af',
        secondaryColor: '#ffffff',
        tertiaryColor: '#ffffff',
    }
});

interface Props {
    currentStatus: string;
}

export default function StateMachineDiagram({ currentStatus }: Props) {
    const containerRef = useRef<HTMLDivElement>(null);

    const generateDefinition = (activeState: string) => {
        return `

        stateDiagram
        direction TB
        [*] --> Pending
        Pending --> OnHold:pendingBio
        Pending --> PendingPayment:noVerif 
        Pending --> Cancelled:payFail
        OnHold --> PendingPayment:bioSuccess
        OnHold --> Cancelled:verifFail
        PendingPayment --> Confirmed:paySuccess
        Confirmed --> Processing:prepShip
        Processing --> Shipped:dispatch
        Shipped --> Delivered:received
        Shipped --> OnHold:deliveryIssue
        Delivered --> Returning:returnInit
        Returning --> Returned:itemBack
        Returned --> Refunded:refundDone
        PendingPayment --> Cancelled:cancel
        Confirmed --> Cancelled:cancel
        Processing --> Cancelled:cancel
        Shipped --> Cancelled:cancel

        %% Highlighting logic
        class ${activeState} active
        classDef active fill:#3b82f6,color:#fff,stroke:#1d4ed8,stroke-width:4px,font-weight:bold
    `;
    };

    useEffect(() => {
        if (containerRef.current && currentStatus) {
            // Clear previous diagram
            containerRef.current.removeAttribute('data-processed');

            const definition = generateDefinition(currentStatus);

            // Render the new diagram
            mermaid.render('mermaid-svg', definition).then((result) => {
                if (containerRef.current) {
                    containerRef.current.innerHTML = result.svg;
                }
            });
        }
    }, [currentStatus]);

    return (
        <div className="w-full bg-white p-6 rounded-xl border border-gray-100 shadow-sm overflow-x-auto">
            <h3 className="text-lg font-bold text-gray-700 mb-4 text-center">Live Transition Map</h3>
            <div className="w-full bg-slate-50 p-8 rounded-2xl border border-slate-200 shadow-inner overflow-hidden">
                <div
                    ref={containerRef}
                    className="flex justify-center items-center min-h-[300px]"
                    id="mermaid-container"
                />
            </div>
            <p className="text-center text-xs text-gray-400 mt-4 italic">
                Blue node represents the current status of order in real-time.
            </p>
        </div>
    );
}
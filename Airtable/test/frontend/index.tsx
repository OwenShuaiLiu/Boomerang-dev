import {initializeBlock} from '@airtable/blocks/ui';
import React from 'react';

function HelloWorldTypescriptBlock() {
    // YOUR CODE GOES HERE
    fetch('http://54.185.214.54:5000/confirm_consignment', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "api_key": "boomerang2020v1"
        })
        })
    return <div>Hello world 🚀</div>;
}

initializeBlock(() => <HelloWorldTypescriptBlock />);

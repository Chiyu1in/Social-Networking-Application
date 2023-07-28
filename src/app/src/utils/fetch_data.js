export async function postData(url, data) {
   
    try {
      const tokenInfo = JSON.parse(localStorage.getItem("tokenInfo"))
      const response = await fetch(url, {
        body: JSON.stringify(data),
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'content-type': 'application/json',
          'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,
        },
        method: 'POST',
        mode: 'cors',
        redirect: 'follow',
        referrer: 'no-referrer', // *client, no-referrer
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      return console.error('Error:', error);
    }
  }

export async function getData(url) {
  
  try {
    const tokenInfo = JSON.parse(localStorage.getItem("tokenInfo"))
    const response = await fetch(url, {
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,
      },
      method: 'GET',
      mode: 'cors',
      redirect: 'follow',
      referrer: 'no-referrer', // *client, no-referrer
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    return console.error('Error:', error);
  }
}

export async function patchData(url, data) {
  
  try {
    const tokenInfo = JSON.parse(localStorage.getItem("tokenInfo"))
    const response = await fetch(url, {
      body: JSON.stringify(data),
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'content-type': 'application/json',
        'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,
      },
      method: 'PATCH',
      mode: 'cors',
      redirect: 'follow',
      referrer: 'no-referrer', // *client, no-referrer
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    return console.error('Error:', error);
  }
}

export async function putData(url, data) {
  
  try {
    const tokenInfo = JSON.parse(localStorage.getItem("tokenInfo"))
    const response = await fetch(url, {
      body: JSON.stringify(data),
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'content-type': 'application/json',
        'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,
      },
      method: 'PUT',
      mode: 'cors',
      redirect: 'follow',
      referrer: 'no-referrer', // *client, no-referrer
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    return console.error('Error:', error);
  }
}
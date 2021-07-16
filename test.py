    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "recaptcha-anchor")))
    ele = driver.find_element(By.ID, "recaptcha-anchor")
    #ActionChains(driver).move_to_element(ele).perform()
    ele.click()
    driver.switch_to.default_content()  

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title=\"recaptcha challenge\"]")))
    iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title=\"recaptcha challenge\"]")
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "rc-imageselect")))
    
    if ATTACK_IMAGES:
        image_recaptcha(driver)



elif ATTACK_AUDIO:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "recaptcha-audio-button")))
        time.sleep(1)
        driver.find_element(By.ID, "recaptcha-audio-button").click()

        guess_again = True

        while guess_again:
            init("audio")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "audio-source")))
            # Parse table details offline
            body = driver.find_element(By.CSS_SELECTOR, "body").get_attribute('innerHTML').encode("utf8")
            soup = BeautifulSoup(body, 'html.parser')
            link = soup.findAll("a", {"class": "rc-audiochallenge-tdownload-link"})[0]
            urllib.urlretrieve(link["href"], TASK_PATH + "/" + TASK + ".mp3")
            guess_str = get_numbers(TASK_PATH + "/" + TASK, TASK_PATH + "/")
            type_style(driver, "audio-response", guess_str)
            # results.append(guess_str)
            wait_between(0.5, 3)
            driver.find_element(By.ID, "recaptcha-verify-button").click()
            wait_between(1, 2.5)
            try:
                logging.debug("Checking if Google wants us to solve more...")
                driver.switch_to.default_content()
                driver.switch_to.frame(iframeSwitch)
                checkmark_pos = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-checkmark").get_attribute("style")
                guess_again = not (checkmark_pos == "background-position: 0 -600px")
                driver.switch_to.default_content()
                iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title=\"recaptcha challenge\"]")
                driver.switch_to.frame(iframe)
            except Exception as e:
                print e
                guess_again = False
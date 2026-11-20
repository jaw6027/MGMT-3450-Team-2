import { test, expect } from "@playwright/test";

test("page loads local assets and exposes complete company information", async ({
  page,
}) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("response", (response) => {
    if (response.status() >= 400)
      errors.push(`${response.status()} ${response.url()}`);
  });
  await page.goto("/");
  await expect(page).toHaveTitle(/Saif Industries/);
  await expect(page.getByRole("heading", { level: 1 })).toContainText(
    "The right part.",
  );
  await expect(page.locator(".capability-card")).toHaveCount(6);
  await expect(page.locator(".hero-image")).toHaveJSProperty("complete", true);
  expect(
    await page.locator(".hero-image").evaluate((image) => image.naturalWidth),
  ).toBeGreaterThan(0);
  await expect(page.locator(".contact-details")).toContainText(
    "sales@saifind.com",
  );
  await expect(page.locator(".contact-details")).toContainText("661-638-0786");
  await expect(page.locator(".contact-details")).toContainText("1ZGP6");
  const unresolvedAnchors = await page
    .locator('a[href^="#"]')
    .evaluateAll((links) =>
      links
        .filter(
          (link) => link.hash && !document.getElementById(link.hash.slice(1)),
        )
        .map((link) => link.hash),
    );
  expect(unresolvedAnchors).toEqual([]);
  expect(errors).toEqual([]);
});

test("part inquiry carries the visitor’s input into a validated quote form", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByLabel("Part number or description", { exact: true })
    .first()
    .fill("TEST-PART-42");
  await page.getByRole("button", { name: "Find my part" }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();
  await expect(dialog.getByLabel("Part number or description")).toHaveValue(
    "TEST-PART-42",
  );
  await dialog.getByRole("button", { name: "Prepare my inquiry" }).click();
  await expect(page.locator("#quote-review")).toBeHidden();
  await expect(page.locator("#quote-form")).toBeVisible();
  await dialog.getByLabel("Your name").fill("Test Buyer");
  await dialog.getByLabel("Company", { exact: true }).fill("Example Aviation");
  await dialog.getByLabel("Work email").fill("buyer@example.com");
  await dialog.getByLabel("Quantity", { exact: true }).fill("3");
  await dialog.getByLabel("Required condition").selectOption("New surplus");
  await dialog
    .getByLabel("Delivery, documentation & other requirements")
    .fill("Destination: California. Please confirm documentation.");
  await dialog.getByRole("button", { name: "Prepare my inquiry" }).click();
  await expect(page.locator("#quote-review")).toBeVisible();
  await expect(page.locator("#quote-form")).toBeHidden();
  const draft = new URL(
    await page
      .getByRole("link", { name: "Open email draft" })
      .getAttribute("href"),
  );
  expect(draft.protocol).toBe("mailto:");
  expect(draft.pathname).toBe("sales@saifind.com");
  expect(draft.searchParams.get("subject")).toContain("Example Aviation");
  const body = draft.searchParams.get("body");
  for (const value of [
    "TEST-PART-42",
    "Quantity: 3",
    "New surplus",
    "buyer@example.com",
    "Destination: California",
  ])
    expect(body).toContain(value);
  await page.getByRole("button", { name: "Edit details" }).click();
  await expect(dialog.getByLabel("Company", { exact: true })).toHaveValue(
    "Example Aviation",
  );
  await expect(dialog.getByLabel("Part number or description")).toHaveValue(
    "TEST-PART-42",
  );
});

test("inquiry preview can be copied without submitting data", async ({
  page,
  context,
}) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.goto("/");
  await page.locator(".header-quote").click();
  const dialog = page.getByRole("dialog");
  await dialog.getByLabel("Your name").fill("Test Buyer");
  await dialog.getByLabel("Company", { exact: true }).fill("Example Company");
  await dialog.getByLabel("Work email").fill("buyer@example.com");
  await dialog.getByLabel("Part number or description").fill("TEST-PART");
  await dialog.getByLabel("Quantity", { exact: true }).fill("1");
  await dialog.getByRole("button", { name: "Prepare my inquiry" }).click();
  await page.getByRole("button", { name: "Copy inquiry" }).click();
  await expect(page.getByRole("status")).toContainText("Copied.");
  expect(await page.evaluate(() => navigator.clipboard.readText())).toContain(
    "TEST-PART",
  );
  await expect(
    page.getByRole("heading", { name: "Your inquiry is ready." }),
  ).toBeVisible();
});

test("service inquiry opens the correct context and closes accessibly", async ({
  page,
}) => {
  await page.goto("/");
  const trigger = page.getByRole("button", { name: "Check availability" });
  await trigger.click();
  await expect(
    page.getByRole("dialog").getByLabel("Part number or description"),
  ).toHaveValue("Inventory availability inquiry");
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await expect(trigger).toBeFocused();
  await page.getByRole("button", { name: "Talk requirements" }).click();
  await expect(
    page.getByRole("dialog").getByLabel("Part number or description"),
  ).toHaveValue("Quality and documentation inquiry");
  await page.getByRole("button", { name: "Close quote request" }).click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
});

test("FAQs reveal the answer and navigation works on the current viewport", async ({
  page,
  isMobile,
}) => {
  await page.goto("/");
  if (isMobile) {
    const menu = page.locator(".menu-toggle");
    await menu.click();
    await expect(menu).toHaveAttribute("aria-expanded", "true");
  }
  await page
    .getByRole("navigation")
    .getByRole("link", { name: "Our capabilities" })
    .click();
  await expect(page).toHaveURL(/#capabilities$/);
  if (isMobile)
    await expect(
      page.getByRole("button", { name: "Open navigation" }),
    ).toHaveAttribute("aria-expanded", "false");
  const question = page
    .locator("summary")
    .filter({ hasText: "What information do I need for a quote?" });
  await question.click();
  await expect(page.locator("details").first()).toHaveAttribute("open", "");
  await expect(page.locator("details").first().locator("p")).toBeVisible();
});

test("layout stays within the viewport at common phone, tablet and desktop widths", async ({
  page,
}) => {
  await page.goto("/");
  await page.evaluate(() => document.fonts.ready);
  for (const width of [320, 390, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - window.innerWidth,
    );
    expect(overflow, `Overflow at ${width}px`).toBeLessThanOrEqual(1);
  }
});
